package com.tsintergy.chandao.client;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.tsintergy.chandao.config.ChandaoConfig;
import com.tsintergy.chandao.model.Attachment;
import com.tsintergy.chandao.model.Story;
import com.tsintergy.chandao.model.Task;
import com.tsintergy.chandao.model.Bug;
import okhttp3.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

/**
 * 禅道API客户端
 * 
 * 【安全约束】只允许查询操作，禁止新增/修改/删除
 * - 允许：登录、查看详情、下载附件
 * - 禁止：创建、更新、删除、指派、关闭等写操作
 */
public class ChandaoClient {
    
    // ==================== 安全约束 ====================
    // 本客户端仅支持只读操作，以下操作被禁止：
    // - 创建需求/任务/Bug
    // - 更新任何字段
    // - 删除任何数据
    // - 指派、关闭、解决等状态变更
    // ==================================================
    
    private static final Logger log = LoggerFactory.getLogger(ChandaoClient.class);
    
    private final ChandaoConfig config;
    private final OkHttpClient httpClient;
    private final ObjectMapper objectMapper;
    
    private String sessionCookie;
    private boolean loggedIn = false;
    
    public ChandaoClient(ChandaoConfig config) {
        this.config = config;
        this.objectMapper = new ObjectMapper();
        // 忽略未知属性，避免禅道API返回额外字段导致解析失败
        this.objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        this.httpClient = new OkHttpClient.Builder()
                .connectTimeout(config.getConnectTimeout(), TimeUnit.MILLISECONDS)
                .readTimeout(config.getReadTimeout(), TimeUnit.MILLISECONDS)
                .followRedirects(true)
                .followSslRedirects(true)
                .build();
    }
    
    /**
     * 登录禅道
     */
    public boolean login() throws IOException {
        if (loggedIn) {
            return true;
        }
        
        String url = config.getBaseUrl() + "/user-login.json";
        
        FormBody formBody = new FormBody.Builder()
                .add("account", config.getUsername())
                .add("password", config.getPassword())
                .add("keepLogin", "1")
                .build();
        
        Request request = new Request.Builder()
                .url(url)
                .post(formBody)
                .build();
        
        try (Response response = httpClient.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("登录失败: HTTP " + response.code());
            }
            
            // 获取session cookie
            Headers headers = response.headers();
            for (String cookie : headers.values("Set-Cookie")) {
                if (cookie.contains("zentaosid") || cookie.contains("sid")) {
                    sessionCookie = cookie.split(";")[0];
                    break;
                }
            }
            
            String body = response.body().string();
            JsonNode root = objectMapper.readTree(body);
            
            if (root.has("result") && "success".equals(root.get("result").asText())) {
                loggedIn = true;
                log.info("登录成功: {}", config.getUsername());
                return true;
            } else if (root.has("status") && "success".equals(root.get("status").asText())) {
                loggedIn = true;
                log.info("登录成功: {}", config.getUsername());
                return true;
            } else {
                String message = root.has("message") ? root.get("message").asText() : "未知错误";
                throw new IOException("登录失败: " + message);
            }
        }
    }
    
    /**
     * 获取需求详情
     */
    public Story getStory(Long id) throws IOException {
        ensureLoggedIn();
        
        String url = config.getBaseUrl() + "/story-view-" + id + ".json";
        String body = fetchJson(url);
        
        JsonNode root = objectMapper.readTree(body);
        
        // 禅道 API 可能返回 data 字段为字符串或对象
        JsonNode data;
        if (root.has("data")) {
            JsonNode dataNode = root.get("data");
            // 如果 data 是字符串，需要再次解析
            if (dataNode.isTextual()) {
                data = objectMapper.readTree(dataNode.asText());
            } else {
                data = dataNode;
            }
        } else {
            data = root;
        }
        
        // 获取 story 节点
        JsonNode storyNode = data.has("story") ? data.get("story") : data;
        
        Story story = new Story();
        
        // 手动解析字段
        if (storyNode.has("id")) {
            story.setId(storyNode.get("id").asLong());
        }
        if (storyNode.has("title")) {
            story.setTitle(storyNode.get("title").asText());
        }
        if (storyNode.has("spec")) {
            story.setSpec(storyNode.get("spec").asText());
        }
        if (storyNode.has("verify")) {
            story.setVerify(storyNode.get("verify").asText());
        }
        if (storyNode.has("status")) {
            story.setStatus(storyNode.get("status").asText());
        }
        if (storyNode.has("stage")) {
            story.setStage(storyNode.get("stage").asText());
        }
        if (storyNode.has("pri")) {
            story.setPri(storyNode.get("pri").asText());
        }
        if (storyNode.has("source")) {
            story.setSource(storyNode.get("source").asText());
        }
        if (storyNode.has("category")) {
            story.setCategory(storyNode.get("category").asText());
        }
        if (storyNode.has("product")) {
            story.setProduct(storyNode.get("product").asLong());
        }
        if (storyNode.has("module")) {
            story.setModule(storyNode.get("module").asLong());
        }
        if (storyNode.has("plan")) {
            String plan = storyNode.get("plan").asText();
            if (!plan.isEmpty()) {
                story.setPlan(Long.parseLong(plan));
            }
        }
        if (storyNode.has("project")) {
            story.setProject(storyNode.get("project").asLong());
        }
        if (storyNode.has("openedBy")) {
            story.setOpenedBy(storyNode.get("openedBy").asText());
        }
        if (storyNode.has("openedDate")) {
            story.setOpenedDate(storyNode.get("openedDate").asText());
        }
        if (storyNode.has("assignedTo")) {
            story.setAssignedTo(storyNode.get("assignedTo").asText());
        }
        if (storyNode.has("assignedDate")) {
            story.setAssignedDate(storyNode.get("assignedDate").asText());
        }
        if (storyNode.has("closedBy")) {
            story.setClosedBy(storyNode.get("closedBy").asText());
        }
        if (storyNode.has("closedDate")) {
            story.setClosedDate(storyNode.get("closedDate").asText());
        }
        if (storyNode.has("closedReason")) {
            story.setClosedReason(storyNode.get("closedReason").asText());
        }
        if (storyNode.has("parent")) {
            story.setParent(storyNode.get("parent").asLong());
        }
        if (storyNode.has("version")) {
            story.setVersion(storyNode.get("version").asText());
        }
        if (storyNode.has("deleted")) {
            story.setDeleted(storyNode.get("deleted").asText());
        }
        
        // 解析附件
        if (storyNode.has("files")) {
            story.setAttachments(parseAttachments(storyNode.get("files")));
        }
        
        // 解析产品名称
        if (data.has("product") && data.get("product").isObject() && data.get("product").has("name")) {
            story.setProductName(data.get("product").get("name").asText());
        }
        
        // 解析模块名称
        if (data.has("storyModule") && data.get("storyModule").isObject() && data.get("storyModule").has("name")) {
            story.setModuleName(data.get("storyModule").get("name").asText());
        }
        
        log.info("获取需求: {} - {}", id, story.getTitle());
        return story;
    }
    
    /**
     * 获取任务详情
     */
    public Task getTask(Long id) throws IOException {
        ensureLoggedIn();

        String url = config.getBaseUrl() + "/task-view-" + id + ".json";
        String body = fetchJson(url);

        JsonNode root = objectMapper.readTree(body);

        // 禅道 API 可能返回 data 字段为字符串或对象
        JsonNode data;
        if (root.has("data")) {
            JsonNode dataNode = root.get("data");
            // 如果 data 是字符串，需要再次解析
            if (dataNode.isTextual()) {
                data = objectMapper.readTree(dataNode.asText());
            } else {
                data = dataNode;
            }
        } else {
            data = root;
        }

        // 禅道API返回嵌套格式
        JsonNode taskNode = data.has("task") ? data.get("task") : data;

        Task task = objectMapper.treeToValue(taskNode, Task.class);

        if (taskNode.has("files")) {
            task.setAttachments(parseAttachments(taskNode.get("files")));
        }

        log.info("获取任务: {} - {}", id, task.getName());
        return task;
    }
    
    /**
     * 获取Bug详情
     */
    public Bug getBug(Long id) throws IOException {
        ensureLoggedIn();

        String url = config.getBaseUrl() + "/bug-view-" + id + ".json";
        String body = fetchJson(url);

        JsonNode root = objectMapper.readTree(body);

        // 禅道 API 可能返回 data 字段为字符串或对象
        JsonNode data;
        if (root.has("data")) {
            JsonNode dataNode = root.get("data");
            // 如果 data 是字符串，需要再次解析
            if (dataNode.isTextual()) {
                data = objectMapper.readTree(dataNode.asText());
            } else {
                data = dataNode;
            }
        } else {
            data = root;
        }

        // 禅道API返回嵌套格式
        JsonNode bugNode = data.has("bug") ? data.get("bug") : data;

        Bug bug = objectMapper.treeToValue(bugNode, Bug.class);

        if (bugNode.has("files")) {
            bug.setAttachments(parseAttachments(bugNode.get("files")));
        }

        log.info("获取Bug: {} - {}", id, bug.getTitle());
        return bug;
    }
    
    /**
     * 下载附件
     */
    public InputStream downloadAttachment(Long attachmentId) throws IOException {
        ensureLoggedIn();
        
        String url = config.getBaseUrl() + "/file-download-" + attachmentId + ".json";
        
        Request.Builder requestBuilder = new Request.Builder().url(url);
        if (sessionCookie != null) {
            requestBuilder.addHeader("Cookie", sessionCookie);
        }
        
        Response response = httpClient.newCall(requestBuilder.build()).execute();
        if (!response.isSuccessful()) {
            throw new IOException("下载附件失败: HTTP " + response.code());
        }
        
        return response.body().byteStream();
    }
    
    /**
     * 下载图片（从禅道文件路径）
     */
    public InputStream downloadImage(String imagePath) throws IOException {
        ensureLoggedIn();
        
        String url;
        if (imagePath.startsWith("http")) {
            url = imagePath;
        } else {
            url = config.getBaseUrl() + "/" + imagePath;
        }
        
        Request.Builder requestBuilder = new Request.Builder().url(url);
        if (sessionCookie != null) {
            requestBuilder.addHeader("Cookie", sessionCookie);
        }
        
        Response response = httpClient.newCall(requestBuilder.build()).execute();
        if (!response.isSuccessful()) {
            throw new IOException("下载图片失败: HTTP " + response.code());
        }
        
        return response.body().byteStream();
    }
    
    private String fetchJson(String url) throws IOException {
        Request.Builder requestBuilder = new Request.Builder().url(url);
        if (sessionCookie != null) {
            requestBuilder.addHeader("Cookie", sessionCookie);
        }
        
        try (Response response = httpClient.newCall(requestBuilder.build()).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("请求失败: " + url + " HTTP " + response.code());
            }
            return response.body().string();
        }
    }
    
    private List<Attachment> parseAttachments(JsonNode filesNode) {
        List<Attachment> attachments = new ArrayList<>();
        if (filesNode != null && filesNode.isObject()) {
            filesNode.fields().forEachRemaining(entry -> {
                try {
                    Attachment att = objectMapper.treeToValue(entry.getValue(), Attachment.class);
                    attachments.add(att);
                } catch (Exception e) {
                    log.warn("解析附件失败: {}", e.getMessage());
                }
            });
        }
        return attachments;
    }
    
    private void ensureLoggedIn() throws IOException {
        if (!loggedIn) {
            login();
        }
    }
    
    public boolean isLoggedIn() {
        return loggedIn;
    }
}