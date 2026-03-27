package com.tsintergy.chandao.service;

import com.tsintergy.chandao.cli.CommandLineArgs;
import com.tsintergy.chandao.client.ChandaoClient;
import com.tsintergy.chandao.config.ChandaoConfig;
import com.tsintergy.chandao.model.Attachment;
import com.tsintergy.chandao.model.Story;
import com.tsintergy.chandao.model.Task;
import com.tsintergy.chandao.model.Bug;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * 禅道服务主类
 */
public class ChandaoService {
    
    private static final Logger log = LoggerFactory.getLogger(ChandaoService.class);
    
    private final ChandaoConfig config;
    private final ChandaoClient client;
    private final MarkdownExporter exporter;
    
    public ChandaoService(ChandaoConfig config) {
        this.config = config;
        this.client = new ChandaoClient(config);
        this.exporter = new MarkdownExporter(config.getOutputDir());
    }
    
    /**
     * 执行命令
     */
    public void execute(CommandLineArgs args) throws Exception {
        // 登录
        if (!client.login()) {
            throw new Exception("登录失败");
        }
        
        // 根据命令执行不同操作
        List<Long> idList = args.getIdList();
        
        if (!idList.isEmpty()) {
            // 单个或批量下载
            for (Long id : idList) {
                fetchById(id, args);
            }
        } else if (args.getProjectId() != null) {
            // 项目下载
            fetchProject(args.getProjectId(), args);
        } else {
            throw new Exception("请指定要下载的ID或项目");
        }
    }
    
    private void fetchById(Long id, CommandLineArgs args) throws Exception {
        String type = args.getType().toLowerCase();

        Path attachDir = Paths.get(config.getOutputDir(), "attachments", type, id.toString());
        Files.createDirectories(attachDir);

        switch (type) {
            case "story":
                Story story = client.getStory(id);
                downloadAttachments(story.getAttachments(), "story", id, args);
                // 下载内容中的图片
                downloadContentImages(story.getSpec(), attachDir);
                downloadContentImages(story.getVerify(), attachDir);
                exporter.exportStory(story);
                break;
            case "task":
                Task task = client.getTask(id);
                downloadAttachments(task.getAttachments(), "task", id, args);
                // 下载内容中的图片
                downloadContentImages(task.getDesc(), attachDir);
                exporter.exportTask(task);
                break;
            case "bug":
                Bug bug = client.getBug(id);
                downloadAttachments(bug.getAttachments(), "bug", id, args);
                // 下载内容中的图片
                downloadContentImages(bug.getSteps(), attachDir);
                exporter.exportBug(bug);
                break;
            default:
                throw new Exception("未知类型: " + type);
        }
    }
    
    private void fetchProject(Long projectId, CommandLineArgs args) throws Exception {
        // TODO: 实现项目全量下载
        throw new Exception("项目下载功能待实现");
    }
    
    /**
     * 下载附件
     */
    private void downloadAttachments(List<Attachment> attachments, String type, Long id, CommandLineArgs args) {
        if (attachments == null || attachments.isEmpty()) {
            return;
        }

        if (args.isNoAttachment() && args.isNoImage()) {
            return;
        }

        Path attachDir = Paths.get(config.getOutputDir(), "attachments", type, id.toString());
        try {
            Files.createDirectories(attachDir);
        } catch (IOException e) {
            log.error("创建目录失败: {}", attachDir, e);
            return;
        }

        for (Attachment att : attachments) {
            try {
                boolean isImage = att.isImage();

                // 跳过图片或附件
                if (isImage && args.isNoImage()) continue;
                if (!isImage && args.isNoAttachment()) continue;

                Path targetPath = attachDir.resolve(att.getFileName());

                try (InputStream is = client.downloadAttachment(att.getId())) {
                    Files.copy(is, targetPath);
                    att.setLocalPath(targetPath.toString());
                    log.info("下载附件: {} -> {}", att.getFileName(), targetPath);
                }
            } catch (Exception e) {
                log.error("下载附件失败: {} - {}", att.getId(), att.getTitle(), e);
            }
        }
    }

    /**
     * 下载内容中的图片
     * @param content 包含HTML的内容
     * @param attachDir 附件保存目录
     */
    private void downloadContentImages(String content, Path attachDir) {
        if (content == null || content.isEmpty()) {
            return;
        }

        try {
            Files.createDirectories(attachDir);
        } catch (IOException e) {
            log.error("创建目录失败: {}", attachDir, e);
            return;
        }

        // 匹配 <img src="xxx" /> 标签
        Pattern pattern = Pattern.compile("<img[^>]+src=\"([^\"]+)\"[^>]*>");
        Matcher matcher = pattern.matcher(content);

        while (matcher.find()) {
            String src = matcher.group(1);
            try {
                // 提取文件名
                String filename = src.substring(src.lastIndexOf('/') + 1);
                if (filename.isEmpty()) {
                    continue;
                }

                Path targetPath = attachDir.resolve(filename);

                // 如果文件已存在，跳过
                if (Files.exists(targetPath)) {
                    continue;
                }

                // 下载图片
                try (InputStream is = client.downloadImage(src)) {
                    Files.copy(is, targetPath);
                    log.info("下载图片: {} -> {}", filename, targetPath);
                }
            } catch (Exception e) {
                log.error("下载图片失败: {}", src, e);
            }
        }
    }
}