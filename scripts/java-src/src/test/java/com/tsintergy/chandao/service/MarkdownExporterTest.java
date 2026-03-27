package com.tsintergy.chandao.service;

import com.tsintergy.chandao.model.Attachment;
import com.tsintergy.chandao.model.Story;
import com.tsintergy.chandao.model.Task;
import com.tsintergy.chandao.model.Bug;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;

import static org.junit.Assert.*;

/**
 * MarkdownExporter 单元测试
 */
public class MarkdownExporterTest {

    private Path tempOutputDir;
    private MarkdownExporter exporter;

    @Before
    public void setUp() throws IOException {
        tempOutputDir = Files.createTempDirectory("markdown-export-test");
        exporter = new MarkdownExporter(tempOutputDir.toString());
    }

    @After
    public void tearDown() throws IOException {
        deleteDirectory(tempOutputDir.toFile());
    }

    private void deleteDirectory(File dir) {
        if (dir.isDirectory()) {
            for (File file : dir.listFiles()) {
                deleteDirectory(file);
            }
        }
        dir.delete();
    }

    @Test
    public void testExportStory() throws IOException {
        Story story = new Story();
        story.setId(123L);
        story.setTitle("用户登录功能");
        story.setStatus("active");
        story.setStage("wait");
        story.setPri("1");
        story.setSpec("实现用户登录功能");
        story.setVerify("1. 能正常登录\n2. 错误提示正确");

        exporter.exportStory(story);

        // 文件名格式：ID-标题.md
        Path storyFile = tempOutputDir.resolve("story/123-用户登录功能.md");
        assertTrue(Files.exists(storyFile));

        String content = new String(Files.readAllBytes(storyFile));
        assertTrue(content.contains("【用户登录功能】123"));
        assertTrue(content.contains("类型: 需求"));
        assertTrue(content.contains("active"));
        assertTrue(content.contains("实现用户登录功能"));
        assertTrue(content.contains("验收标准"));
    }

    @Test
    public void testExportStory_WithProductName() throws IOException {
        Story story = new Story();
        story.setId(124L);
        story.setTitle("需求标题");
        story.setProductName("产品A");

        exporter.exportStory(story);

        Path storyFile = tempOutputDir.resolve("story/124-需求标题.md");
        String content = new String(Files.readAllBytes(storyFile));
        assertTrue(content.contains("产品A"));
    }

    @Test
    public void testExportStory_WithAttachments() throws IOException {
        Story story = new Story();
        story.setId(125L);
        story.setTitle("带附件的需求");

        Attachment att1 = new Attachment();
        att1.setId(1L);
        att1.setTitle("document.pdf");
        att1.setExtension("pdf");

        Attachment att2 = new Attachment();
        att2.setId(2L);
        att2.setTitle("screenshot.png");
        att2.setExtension("png");

        story.setAttachments(Arrays.asList(att1, att2));

        exporter.exportStory(story);

        Path storyFile = tempOutputDir.resolve("story/125-带附件的需求.md");
        String content = new String(Files.readAllBytes(storyFile));
        assertTrue(content.contains("附件"));
        assertTrue(content.contains("document.pdf"));
        assertTrue(content.contains("screenshot.png"));
    }

    @Test
    public void testExportTask() throws IOException {
        Task task = new Task();
        task.setId(456L);
        task.setName("实现登录接口");
        task.setStatus("doing");
        task.setType("devel");
        task.setPri("2");
        task.setDesc("实现 RESTful 登录接口");
        task.setEstimate(8.0f);
        task.setConsumed(4.0f);

        exporter.exportTask(task);

        Path taskFile = tempOutputDir.resolve("task/456-实现登录接口.md");
        assertTrue("文件应该存在: " + taskFile, Files.exists(taskFile));

        String content = new String(Files.readAllBytes(taskFile));
        assertTrue("内容应包含标题", content.contains("【实现登录接口】456"));
        assertTrue("内容应包含类型", content.contains("类型: 任务"));
        assertTrue("内容应包含状态", content.contains("doing"));
        assertTrue("内容应包含工时信息", content.contains("预计工时"));
    }

    @Test
    public void testExportTask_WithStoryTitle() throws IOException {
        Task task = new Task();
        task.setId(457L);
        task.setName("任务名");
        task.setStoryTitle("相关需求标题");

        exporter.exportTask(task);

        Path taskFile = tempOutputDir.resolve("task/457-任务名.md");
        String content = new String(Files.readAllBytes(taskFile));
        assertTrue(content.contains("相关需求"));
        assertTrue(content.contains("相关需求标题"));
    }

    @Test
    public void testExportTask_WithDeadline() throws IOException {
        Task task = new Task();
        task.setId(458L);
        task.setName("紧急任务");
        task.setDeadline("2024-12-31");

        exporter.exportTask(task);

        Path taskFile = tempOutputDir.resolve("task/458-紧急任务.md");
        String content = new String(Files.readAllBytes(taskFile));
        assertTrue(content.contains("截止日期"));
        assertTrue(content.contains("2024-12-31"));
    }

    @Test
    public void testExportBug() throws IOException {
        Bug bug = new Bug();
        bug.setId(789L);
        bug.setTitle("登录页面崩溃");
        bug.setStatus("active");
        bug.setSeverity("3");
        bug.setPri("1");
        bug.setType("codeerror");
        bug.setSteps("1. 打开登录页\n2. 点击提交\n3. 页面崩溃");

        exporter.exportBug(bug);

        Path bugFile = tempOutputDir.resolve("bug/789-登录页面崩溃.md");
        assertTrue(Files.exists(bugFile));

        String content = new String(Files.readAllBytes(bugFile));
        assertTrue(content.contains("【登录页面崩溃】789"));
        assertTrue(content.contains("类型: Bug"));
        assertTrue(content.contains("严重程度"));
        assertTrue(content.contains("重现步骤"));
    }

    @Test
    public void testExportBug_WithResolution() throws IOException {
        Bug bug = new Bug();
        bug.setId(790L);
        bug.setTitle("已解决Bug");
        bug.setResolvedBy("developer");
        bug.setResolvedDate("2024-01-20 10:00:00");
        bug.setResolution("fixed");

        exporter.exportBug(bug);

        Path bugFile = tempOutputDir.resolve("bug/790-已解决Bug.md");
        String content = new String(Files.readAllBytes(bugFile));
        assertTrue(content.contains("解决人"));
        assertTrue(content.contains("developer"));
        assertTrue(content.contains("解决方案"));
    }

    @Test
    public void testExportBug_WithAttachments() throws IOException {
        Bug bug = new Bug();
        bug.setId(791L);
        bug.setTitle("带截图的Bug");

        Attachment screenshot = new Attachment();
        screenshot.setId(1L);
        screenshot.setTitle("error.png");
        screenshot.setExtension("png");

        bug.setAttachments(Arrays.asList(screenshot));

        exporter.exportBug(bug);

        Path bugFile = tempOutputDir.resolve("bug/791-带截图的Bug.md");
        String content = new String(Files.readAllBytes(bugFile));
        assertTrue(content.contains("error.png"));
        assertTrue(content.contains("![error.png]"));
    }

    @Test
    public void testExportStory_NullFields() throws IOException {
        Story story = new Story();
        story.setId(999L);
        story.setTitle("最小需求");
        // 其他字段为 null

        exporter.exportStory(story);

        Path storyFile = tempOutputDir.resolve("story/999-最小需求.md");
        assertTrue(Files.exists(storyFile));

        String content = new String(Files.readAllBytes(storyFile));
        assertTrue(content.contains("【最小需求】999"));
        // null 字段应显示为 "-"
        assertTrue(content.contains("| - |"));
    }

    @Test
    public void testExportStory_ImageInContent() throws IOException {
        Story story = new Story();
        story.setId(888L);
        story.setTitle("含图片的需求");
        story.setSpec("描述内容 <img src=\"data/upload/2024/image.png\" /> 继续内容");

        exporter.exportStory(story);

        Path storyFile = tempOutputDir.resolve("story/888-含图片的需求.md");
        String content = new String(Files.readAllBytes(storyFile));
        assertTrue(content.contains("![](attachments/image.png)"));
    }

    @Test
    public void testExportStory_MultipleImages() throws IOException {
        Story story = new Story();
        story.setId(887L);
        story.setTitle("多图片需求");
        story.setSpec("第一张 <img src=\"img1.png\" /> 第二张 <img src=\"img2.jpg\" />");

        exporter.exportStory(story);

        Path storyFile = tempOutputDir.resolve("story/887-多图片需求.md");
        String content = new String(Files.readAllBytes(storyFile));
        assertTrue(content.contains("img1.png"));
        assertTrue(content.contains("img2.jpg"));
    }

    @Test
    public void testOutputDirectoryCreation() throws IOException {
        // 使用新的不存在的子目录
        Path newOutputDir = tempOutputDir.resolve("new-sub-dir");
        MarkdownExporter newExporter = new MarkdownExporter(newOutputDir.toString());

        Story story = new Story();
        story.setId(111L);
        story.setTitle("测试");

        newExporter.exportStory(story);

        assertTrue(Files.exists(newOutputDir.resolve("story/111-测试.md")));
    }

    @Test
    public void testChineseCharacters() throws IOException {
        Story story = new Story();
        story.setId(222L);
        story.setTitle("中文标题测试");
        story.setSpec("中文描述，包含特殊字符：、。！？");
        story.setCategory("功能需求");

        exporter.exportStory(story);

        Path storyFile = tempOutputDir.resolve("story/222-中文标题测试.md");
        String content = new String(Files.readAllBytes(storyFile), "UTF-8");
        assertTrue(content.contains("【中文标题测试】222"));
        assertTrue(content.contains("中文描述"));
        assertTrue(content.contains("功能需求"));
    }
}