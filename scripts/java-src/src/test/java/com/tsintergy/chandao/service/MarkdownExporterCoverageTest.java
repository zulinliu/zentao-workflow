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
import java.util.Collections;

import static org.junit.Assert.*;

/**
 * MarkdownExporter 额外测试 - 提高覆盖率
 */
public class MarkdownExporterCoverageTest {

    private Path tempOutputDir;
    private MarkdownExporter exporter;

    @Before
    public void setUp() throws IOException {
        tempOutputDir = Files.createTempDirectory("markdown-coverage-test");
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
    public void testExportStory_EmptySpec() throws IOException {
        Story story = new Story();
        story.setId(100L);
        story.setTitle("空描述需求");
        story.setSpec("");
        story.setVerify("");

        exporter.exportStory(story);

        Path storyFile = tempOutputDir.resolve("story/100-空描述需求.md");
        assertTrue(Files.exists(storyFile));
    }

    @Test
    public void testExportStory_WithProjectName() throws IOException {
        Story story = new Story();
        story.setId(101L);
        story.setTitle("带项目的需求");
        story.setProjectName("测试项目");

        exporter.exportStory(story);

        Path storyFile = tempOutputDir.resolve("story/101-带项目的需求.md");
        String content = new String(Files.readAllBytes(storyFile));
        assertTrue(content.contains("测试项目"));
    }

    @Test
    public void testExportStory_ComplexHtmlInSpec() throws IOException {
        Story story = new Story();
        story.setId(103L);
        story.setTitle("复杂HTML");
        story.setSpec("<p>段落1</p><img src=\"/path/to/image1.png\" /><p>段落2</p><img src=\"data/upload/image2.jpg\" />");

        exporter.exportStory(story);

        Path storyFile = tempOutputDir.resolve("story/103-复杂HTML.md");
        String content = new String(Files.readAllBytes(storyFile));
        assertTrue(content.contains("image1.png"));
    }

    @Test
    public void testExportTask_WithAllFields() throws IOException {
        Task task = new Task();
        task.setId(200L);
        task.setName("完整任务");
        task.setStatus("done");
        task.setType("test");
        task.setPri("1");
        task.setDesc("任务描述");
        task.setEstimate(16.0f);
        task.setConsumed(8.0f);
        task.setDeadline("2024-12-31");

        exporter.exportTask(task);

        Path taskFile = tempOutputDir.resolve("task/200-完整任务.md");
        String content = new String(Files.readAllBytes(taskFile));
        assertTrue(content.contains("done"));
    }

    @Test
    public void testExportTask_WithAttachments() throws IOException {
        Task task = new Task();
        task.setId(202L);
        task.setName("带附件任务");

        Attachment att = new Attachment();
        att.setId(1L);
        att.setTitle("task_doc.pdf");
        att.setExtension("pdf");

        task.setAttachments(Collections.singletonList(att));

        exporter.exportTask(task);

        Path taskFile = tempOutputDir.resolve("task/202-带附件任务.md");
        String content = new String(Files.readAllBytes(taskFile));
        assertTrue(content.contains("task_doc.pdf"));
    }

    @Test
    public void testExportBug_AllFields() throws IOException {
        Bug bug = new Bug();
        bug.setId(300L);
        bug.setTitle("完整Bug");
        bug.setStatus("resolved");
        bug.setSeverity("1");
        bug.setPri("2");
        bug.setType("codeerror");
        bug.setSteps("步骤1\n步骤2");
        bug.setResolvedBy("resolver");
        bug.setResolvedDate("2024-01-02");
        bug.setResolution("fixed");

        exporter.exportBug(bug);

        Path bugFile = tempOutputDir.resolve("bug/300-完整Bug.md");
        String content = new String(Files.readAllBytes(bugFile));
        assertTrue(content.contains("resolver"));
    }

    @Test
    public void testExportBug_WithImageAttachment() throws IOException {
        Bug bug = new Bug();
        bug.setId(302L);
        bug.setTitle("带图片Bug");

        Attachment img = new Attachment();
        img.setId(1L);
        img.setTitle("screenshot.png");
        img.setExtension("png");

        bug.setAttachments(Collections.singletonList(img));

        exporter.exportBug(bug);

        Path bugFile = tempOutputDir.resolve("bug/302-带图片Bug.md");
        String content = new String(Files.readAllBytes(bugFile));
        assertTrue(content.contains("![screenshot.png]"));
    }

    @Test
    public void testFileNameSanitization() throws IOException {
        Story story = new Story();
        story.setId(400L);
        story.setTitle("包含/非法\\字符:的*标题");

        exporter.exportStory(story);

        Path storyDir = tempOutputDir.resolve("story");
        assertTrue(Files.exists(storyDir));
    }

    @Test
    public void testLongFileName() throws IOException {
        Story story = new Story();
        story.setId(401L);
        StringBuilder longTitle = new StringBuilder();
        for (int i = 0; i < 20; i++) {
            longTitle.append("非常长的标题");
        }
        story.setTitle(longTitle.toString());

        exporter.exportStory(story);

        Path storyDir = tempOutputDir.resolve("story");
        assertTrue(Files.exists(storyDir));
    }
}