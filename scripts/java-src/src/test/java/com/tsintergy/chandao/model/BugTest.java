package com.tsintergy.chandao.model;

import org.junit.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;

/**
 * Bug 单元测试
 */
public class BugTest {

    @Test
    public void testGetId() {
        Bug bug = new Bug();
        bug.setId(1L);
        assertEquals(Long.valueOf(1L), bug.getId());
    }

    @Test
    public void testGetTitle() {
        Bug bug = new Bug();
        bug.setTitle("登录页面无法提交");
        assertEquals("登录页面无法提交", bug.getTitle());
    }

    @Test
    public void testGetSteps() {
        Bug bug = new Bug();
        bug.setSteps("1. 打开登录页面\n2. 输入账号密码\n3. 点击登录无反应");
        assertEquals("1. 打开登录页面\n2. 输入账号密码\n3. 点击登录无反应", bug.getSteps());
    }

    @Test
    public void testGetStatus() {
        Bug bug = new Bug();
        bug.setStatus("active");
        assertEquals("active", bug.getStatus());
    }

    @Test
    public void testGetConfirmed() {
        Bug bug = new Bug();
        bug.setConfirmed("1");
        assertEquals("1", bug.getConfirmed());
    }

    @Test
    public void testGetPri() {
        Bug bug = new Bug();
        bug.setPri("1");
        assertEquals("1", bug.getPri());
    }

    @Test
    public void testGetSeverity() {
        Bug bug = new Bug();
        bug.setSeverity("3");
        assertEquals("3", bug.getSeverity());
    }

    @Test
    public void testGetType() {
        Bug bug = new Bug();
        bug.setType("codeerror");
        assertEquals("codeerror", bug.getType());
    }

    @Test
    public void testGetProduct() {
        Bug bug = new Bug();
        bug.setProduct(100L);
        assertEquals(Long.valueOf(100L), bug.getProduct());
    }

    @Test
    public void testGetModule() {
        Bug bug = new Bug();
        bug.setModule(200L);
        assertEquals(Long.valueOf(200L), bug.getModule());
    }

    @Test
    public void testGetProject() {
        Bug bug = new Bug();
        bug.setProject(300L);
        assertEquals(Long.valueOf(300L), bug.getProject());
    }

    @Test
    public void testGetStory() {
        Bug bug = new Bug();
        bug.setStory(400L);
        assertEquals(Long.valueOf(400L), bug.getStory());
    }

    @Test
    public void testGetTask() {
        Bug bug = new Bug();
        bug.setTask(500L);
        assertEquals(Long.valueOf(500L), bug.getTask());
    }

    @Test
    public void testGetOpenedBy() {
        Bug bug = new Bug();
        bug.setOpenedBy("tester");
        assertEquals("tester", bug.getOpenedBy());
    }

    @Test
    public void testGetOpenedDate() {
        Bug bug = new Bug();
        bug.setOpenedDate("2024-01-15 14:00:00");
        assertEquals("2024-01-15 14:00:00", bug.getOpenedDate());
    }

    @Test
    public void testGetAssignedTo() {
        Bug bug = new Bug();
        bug.setAssignedTo("developer");
        assertEquals("developer", bug.getAssignedTo());
    }

    @Test
    public void testGetAssignedDate() {
        Bug bug = new Bug();
        bug.setAssignedDate("2024-01-15 15:00:00");
        assertEquals("2024-01-15 15:00:00", bug.getAssignedDate());
    }

    @Test
    public void testGetResolvedBy() {
        Bug bug = new Bug();
        bug.setResolvedBy("developer");
        assertEquals("developer", bug.getResolvedBy());
    }

    @Test
    public void testGetResolvedDate() {
        Bug bug = new Bug();
        bug.setResolvedDate("2024-01-16 10:00:00");
        assertEquals("2024-01-16 10:00:00", bug.getResolvedDate());
    }

    @Test
    public void testGetResolution() {
        Bug bug = new Bug();
        bug.setResolution("fixed");
        assertEquals("fixed", bug.getResolution());
    }

    @Test
    public void testGetClosedBy() {
        Bug bug = new Bug();
        bug.setClosedBy("tester");
        assertEquals("tester", bug.getClosedBy());
    }

    @Test
    public void testGetClosedDate() {
        Bug bug = new Bug();
        bug.setClosedDate("2024-01-17 09:00:00");
        assertEquals("2024-01-17 09:00:00", bug.getClosedDate());
    }

    @Test
    public void testGetDuplicateBug() {
        Bug bug = new Bug();
        bug.setDuplicateBug(123L);
        assertEquals(Long.valueOf(123L), bug.getDuplicateBug());
    }

    @Test
    public void testGetDeadline() {
        Bug bug = new Bug();
        bug.setDeadline("2024-01-20");
        assertEquals("2024-01-20", bug.getDeadline());
    }

    @Test
    public void testGetDeleted() {
        Bug bug = new Bug();
        bug.setDeleted("0");
        assertEquals("0", bug.getDeleted());
    }

    @Test
    public void testGetProductName() {
        Bug bug = new Bug();
        bug.setProductName("产品管理系统");
        assertEquals("产品管理系统", bug.getProductName());
    }

    @Test
    public void testGetModuleName() {
        Bug bug = new Bug();
        bug.setModuleName("登录模块");
        assertEquals("登录模块", bug.getModuleName());
    }

    @Test
    public void testGetProjectName() {
        Bug bug = new Bug();
        bug.setProjectName("一期项目");
        assertEquals("一期项目", bug.getProjectName());
    }

    @Test
    public void testGetStoryTitle() {
        Bug bug = new Bug();
        bug.setStoryTitle("用户登录功能");
        assertEquals("用户登录功能", bug.getStoryTitle());
    }

    @Test
    public void testGetAttachments() {
        Bug bug = new Bug();
        Attachment att = new Attachment();
        att.setId(1L);
        att.setTitle("screenshot.png");
        List<Attachment> attachments = Arrays.asList(att);
        bug.setAttachments(attachments);
        assertEquals(1, bug.getAttachments().size());
        assertEquals("screenshot.png", bug.getAttachments().get(0).getTitle());
    }

    @Test
    public void testGetImageUrls() {
        Bug bug = new Bug();
        List<String> urls = Arrays.asList("http://example.com/error.png");
        bug.setImageUrls(urls);
        assertEquals(1, bug.getImageUrls().size());
    }

    @Test
    public void testNullValues() {
        Bug bug = new Bug();
        assertNull(bug.getId());
        assertNull(bug.getTitle());
        assertNull(bug.getSteps());
        assertNull(bug.getStatus());
        assertNull(bug.getResolvedBy());
        assertNull(bug.getAttachments());
    }
}