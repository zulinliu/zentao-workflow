package com.tsintergy.chandao.client;

import com.tsintergy.chandao.config.ChandaoConfig;
import com.tsintergy.chandao.model.Attachment;
import com.tsintergy.chandao.model.Story;
import com.tsintergy.chandao.model.Task;
import com.tsintergy.chandao.model.Bug;
import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.MockWebServer;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.IOException;
import java.util.List;

import static org.junit.Assert.*;

/**
 * ChandaoClient 单元测试
 */
public class ChandaoClientTest {

    private MockWebServer mockWebServer;
    private ChandaoClient client;
    private ChandaoConfig config;

    @Before
    public void setUp() throws IOException {
        mockWebServer = new MockWebServer();
        mockWebServer.start();

        String baseUrl = mockWebServer.url("/").toString().replaceAll("/$", "");

        config = new ChandaoConfig();
        config.setBaseUrl(baseUrl);
        config.setUsername("testuser");
        config.setPassword("testpass");

        client = new ChandaoClient(config);
    }

    @After
    public void tearDown() throws IOException {
        mockWebServer.shutdown();
    }

    @Test
    public void testLogin_Success() throws IOException {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .addHeader("Set-Cookie", "zentaosid=test-session-id; Path=/")
            .setBody("{\"result\":\"success\"}"));

        boolean result = client.login();
        assertTrue(result);
        assertTrue(client.isLoggedIn());
    }

    @Test
    public void testLogin_Success_WithStatusField() throws IOException {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .addHeader("Set-Cookie", "zentaosid=test-session-id; Path=/")
            .setBody("{\"status\":\"success\"}"));

        boolean result = client.login();
        assertTrue(result);
        assertTrue(client.isLoggedIn());
    }

    @Test(expected = IOException.class)
    public void testLogin_Failure_401() throws IOException {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(401));

        client.login();
    }

    @Test(expected = IOException.class)
    public void testLogin_Failure_ErrorResponse() throws IOException {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .setBody("{\"result\":\"fail\",\"message\":\"用户名或密码错误\"}"));

        client.login();
    }

    @Test
    public void testGetStory() throws IOException {
        // 先登录
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .addHeader("Set-Cookie", "zentaosid=test-session-id; Path=/")
            .setBody("{\"result\":\"success\"}"));

        // 返回需求数据
        String storyResponse = "{\n" +
            "  \"data\": {\n" +
            "    \"story\": {\n" +
            "      \"id\": 123,\n" +
            "      \"title\": \"用户登录功能\",\n" +
            "      \"spec\": \"实现登录功能\",\n" +
            "      \"status\": \"active\"\n" +
            "    },\n" +
            "    \"product\": {\n" +
            "      \"name\": \"产品A\"\n" +
            "    }\n" +
            "  }\n" +
            "}";
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .setBody(storyResponse));

        client.login();
        Story story = client.getStory(123L);

        assertNotNull(story);
        assertEquals(Long.valueOf(123L), story.getId());
        assertEquals("用户登录功能", story.getTitle());
        assertEquals("active", story.getStatus());
        assertEquals("产品A", story.getProductName());
    }

    @Test
    public void testGetStory_FlatResponse() throws IOException {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .addHeader("Set-Cookie", "zentaosid=test-session-id; Path=/")
            .setBody("{\"result\":\"success\"}"));

        // 扁平结构的响应
        String storyResponse = "{\n" +
            "  \"id\": 456,\n" +
            "  \"title\": \"需求标题\",\n" +
            "  \"status\": \"closed\"\n" +
            "}";
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .setBody(storyResponse));

        client.login();
        Story story = client.getStory(456L);

        assertNotNull(story);
        assertEquals(Long.valueOf(456L), story.getId());
        assertEquals("需求标题", story.getTitle());
    }

    @Test
    public void testGetStory_WithAttachments() throws IOException {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .addHeader("Set-Cookie", "zentaosid=test-session-id; Path=/")
            .setBody("{\"result\":\"success\"}"));

        String storyResponse = "{\n" +
            "  \"data\": {\n" +
            "    \"story\": {\n" +
            "      \"id\": 123,\n" +
            "      \"title\": \"带附件的需求\",\n" +
            "      \"files\": {\n" +
            "        \"1\": {\"id\": 1, \"title\": \"doc.pdf\", \"extension\": \"pdf\"},\n" +
            "        \"2\": {\"id\": 2, \"title\": \"image.png\", \"extension\": \"png\"}\n" +
            "      }\n" +
            "    }\n" +
            "  }\n" +
            "}";
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .setBody(storyResponse));

        client.login();
        Story story = client.getStory(123L);

        assertNotNull(story);
        assertNotNull(story.getAttachments());
        assertEquals(2, story.getAttachments().size());
    }

    @Test
    public void testGetTask() throws IOException {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .addHeader("Set-Cookie", "zentaosid=test-session-id; Path=/")
            .setBody("{\"result\":\"success\"}"));

        String taskResponse = "{\n" +
            "  \"data\": {\n" +
            "    \"task\": {\n" +
            "      \"id\": 789,\n" +
            "      \"name\": \"实现登录接口\",\n" +
            "      \"status\": \"doing\",\n" +
            "      \"estimate\": 8.0\n" +
            "    }\n" +
            "  }\n" +
            "}";
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .setBody(taskResponse));

        client.login();
        Task task = client.getTask(789L);

        assertNotNull(task);
        assertEquals(Long.valueOf(789L), task.getId());
        assertEquals("实现登录接口", task.getName());
        assertEquals(Float.valueOf(8.0f), task.getEstimate());
    }

    @Test
    public void testGetBug() throws IOException {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .addHeader("Set-Cookie", "zentaosid=test-session-id; Path=/")
            .setBody("{\"result\":\"success\"}"));

        String bugResponse = "{\n" +
            "  \"data\": {\n" +
            "    \"bug\": {\n" +
            "      \"id\": 100,\n" +
            "      \"title\": \"登录失败\",\n" +
            "      \"status\": \"active\",\n" +
            "      \"severity\": \"3\"\n" +
            "    }\n" +
            "  }\n" +
            "}";
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .setBody(bugResponse));

        client.login();
        Bug bug = client.getBug(100L);

        assertNotNull(bug);
        assertEquals(Long.valueOf(100L), bug.getId());
        assertEquals("登录失败", bug.getTitle());
        assertEquals("3", bug.getSeverity());
    }

    @Test(expected = IOException.class)
    public void testGetStory_NotFound() throws IOException {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .addHeader("Set-Cookie", "zentaosid=test-session-id; Path=/")
            .setBody("{\"result\":\"success\"}"));

        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(404));

        client.login();
        client.getStory(999L);
    }

    @Test
    public void testDownloadAttachment() throws IOException {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .addHeader("Set-Cookie", "zentaosid=test-session-id; Path=/")
            .setBody("{\"result\":\"success\"}"));

        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .setBody("file content"));

        client.login();
        java.io.InputStream is = client.downloadAttachment(1L);

        assertNotNull(is);
        is.close();
    }

    @Test
    public void testDownloadImage() throws IOException {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .addHeader("Set-Cookie", "zentaosid=test-session-id; Path=/")
            .setBody("{\"result\":\"success\"}"));

        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .setBody("image binary data"));

        client.login();
        java.io.InputStream is = client.downloadImage("data/upload/test.png");

        assertNotNull(is);
        is.close();
    }

    @Test
    public void testDownloadImage_AbsoluteUrl() throws IOException {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .addHeader("Set-Cookie", "zentaosid=test-session-id; Path=/")
            .setBody("{\"result\":\"success\"}"));

        // 启动另一个 mock 服务器模拟外部 URL
        MockWebServer externalServer = new MockWebServer();
        externalServer.start();
        externalServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .setBody("external image"));

        String externalUrl = externalServer.url("/image.png").toString();

        client.login();
        java.io.InputStream is = client.downloadImage(externalUrl);

        assertNotNull(is);
        is.close();
        externalServer.shutdown();
    }

    @Test
    public void testAutoLogin() throws IOException {
        // 第一次调用自动登录
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .addHeader("Set-Cookie", "zentaosid=test-session-id; Path=/")
            .setBody("{\"result\":\"success\"}"));

        String storyResponse = "{\n" +
            "  \"id\": 1,\n" +
            "  \"title\": \"测试\"\n" +
            "}";
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .setBody(storyResponse));

        // 不显式调用 login，getStory 应自动登录
        Story story = client.getStory(1L);
        assertNotNull(story);
    }

    @Test
    public void testDoubleLogin() throws IOException {
        mockWebServer.enqueue(new MockResponse()
            .setResponseCode(200)
            .addHeader("Set-Cookie", "zentaosid=test-session-id; Path=/")
            .setBody("{\"result\":\"success\"}"));

        // 第一次登录
        boolean result1 = client.login();
        assertTrue(result1);

        // 第二次登录应该直接返回 true，不再发请求
        boolean result2 = client.login();
        assertTrue(result2);
    }

    @Test
    public void testIsLoggedIn_Initial() {
        assertFalse(client.isLoggedIn());
    }
}