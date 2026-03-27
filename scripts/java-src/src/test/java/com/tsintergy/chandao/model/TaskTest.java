package com.tsintergy.chandao.model;

import org.junit.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;

/**
 * Task 单元测试
 */
public class TaskTest {

    @Test
    public void testGetId() {
        Task task = new Task();
        task.setId(1L);
        assertEquals(Long.valueOf(1L), task.getId());
    }

    @Test
    public void testGetName() {
        Task task = new Task();
        task.setName("实现登录接口");
        assertEquals("实现登录接口", task.getName());
    }

    @Test
    public void testGetDesc() {
        Task task = new Task();
        task.setDesc("实现RESTful登录接口，返回JWT token");
        assertEquals("实现RESTful登录接口，返回JWT token", task.getDesc());
    }

    @Test
    public void testGetStatus() {
        Task task = new Task();
        task.setStatus("doing");
        assertEquals("doing", task.getStatus());
    }

    @Test
    public void testGetType() {
        Task task = new Task();
        task.setType("devel");
        assertEquals("devel", task.getType());
    }

    @Test
    public void testGetPri() {
        Task task = new Task();
        task.setPri("2");
        assertEquals("2", task.getPri());
    }

    @Test
    public void testGetProject() {
        Task task = new Task();
        task.setProject(100L);
        assertEquals(Long.valueOf(100L), task.getProject());
    }

    @Test
    public void testGetModule() {
        Task task = new Task();
        task.setModule(200L);
        assertEquals(Long.valueOf(200L), task.getModule());
    }

    @Test
    public void testGetStory() {
        Task task = new Task();
        task.setStory(300L);
        assertEquals(Long.valueOf(300L), task.getStory());
    }

    @Test
    public void testGetParent() {
        Task task = new Task();
        task.setParent(50L);
        assertEquals(Long.valueOf(50L), task.getParent());
    }

    @Test
    public void testGetOpenedBy() {
        Task task = new Task();
        task.setOpenedBy("zhangsan");
        assertEquals("zhangsan", task.getOpenedBy());
    }

    @Test
    public void testGetOpenedDate() {
        Task task = new Task();
        task.setOpenedDate("2024-01-15 10:00:00");
        assertEquals("2024-01-15 10:00:00", task.getOpenedDate());
    }

    @Test
    public void testGetAssignedTo() {
        Task task = new Task();
        task.setAssignedTo("lisi");
        assertEquals("lisi", task.getAssignedTo());
    }

    @Test
    public void testGetAssignedDate() {
        Task task = new Task();
        task.setAssignedDate("2024-01-16 09:00:00");
        assertEquals("2024-01-16 09:00:00", task.getAssignedDate());
    }

    @Test
    public void testGetFinishedBy() {
        Task task = new Task();
        task.setFinishedBy("lisi");
        assertEquals("lisi", task.getFinishedBy());
    }

    @Test
    public void testGetFinishedDate() {
        Task task = new Task();
        task.setFinishedDate("2024-01-18 17:00:00");
        assertEquals("2024-01-18 17:00:00", task.getFinishedDate());
    }

    @Test
    public void testGetClosedBy() {
        Task task = new Task();
        task.setClosedBy("wangwu");
        assertEquals("wangwu", task.getClosedBy());
    }

    @Test
    public void testGetClosedDate() {
        Task task = new Task();
        task.setClosedDate("2024-01-20 17:00:00");
        assertEquals("2024-01-20 17:00:00", task.getClosedDate());
    }

    @Test
    public void testGetClosedReason() {
        Task task = new Task();
        task.setClosedReason("done");
        assertEquals("done", task.getClosedReason());
    }

    @Test
    public void testGetEstimate() {
        Task task = new Task();
        task.setEstimate(8.5f);
        assertEquals(Float.valueOf(8.5f), task.getEstimate());
    }

    @Test
    public void testGetConsumed() {
        Task task = new Task();
        task.setConsumed(6.0f);
        assertEquals(Float.valueOf(6.0f), task.getConsumed());
    }

    @Test
    public void testGetLeft() {
        Task task = new Task();
        task.setLeft(2.5f);
        assertEquals(Float.valueOf(2.5f), task.getLeft());
    }

    @Test
    public void testGetDeadline() {
        Task task = new Task();
        task.setDeadline("2024-01-25");
        assertEquals("2024-01-25", task.getDeadline());
    }

    @Test
    public void testGetDeleted() {
        Task task = new Task();
        task.setDeleted("0");
        assertEquals("0", task.getDeleted());
    }

    @Test
    public void testGetProjectName() {
        Task task = new Task();
        task.setProjectName("一期项目");
        assertEquals("一期项目", task.getProjectName());
    }

    @Test
    public void testGetModuleName() {
        Task task = new Task();
        task.setModuleName("用户模块");
        assertEquals("用户模块", task.getModuleName());
    }

    @Test
    public void testGetStoryTitle() {
        Task task = new Task();
        task.setStoryTitle("用户登录功能");
        assertEquals("用户登录功能", task.getStoryTitle());
    }

    @Test
    public void testGetAttachments() {
        Task task = new Task();
        Attachment att = new Attachment();
        att.setId(1L);
        att.setTitle("spec.pdf");
        List<Attachment> attachments = Arrays.asList(att);
        task.setAttachments(attachments);
        assertEquals(1, task.getAttachments().size());
        assertEquals("spec.pdf", task.getAttachments().get(0).getTitle());
    }

    @Test
    public void testGetImageUrls() {
        Task task = new Task();
        List<String> urls = Arrays.asList("http://example.com/screenshot.png");
        task.setImageUrls(urls);
        assertEquals(1, task.getImageUrls().size());
    }

    @Test
    public void testNullValues() {
        Task task = new Task();
        assertNull(task.getId());
        assertNull(task.getName());
        assertNull(task.getDesc());
        assertNull(task.getStatus());
        assertNull(task.getEstimate());
        assertNull(task.getAttachments());
    }
}