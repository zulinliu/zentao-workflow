package com.tsintergy.chandao.model;

import org.junit.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;

/**
 * Story 单元测试
 */
public class StoryTest {

    @Test
    public void testGetId() {
        Story story = new Story();
        story.setId(1L);
        assertEquals(Long.valueOf(1L), story.getId());
    }

    @Test
    public void testGetTitle() {
        Story story = new Story();
        story.setTitle("用户登录功能");
        assertEquals("用户登录功能", story.getTitle());
    }

    @Test
    public void testGetSpec() {
        Story story = new Story();
        story.setSpec("实现用户登录功能，支持账号密码和手机验证码");
        assertEquals("实现用户登录功能，支持账号密码和手机验证码", story.getSpec());
    }

    @Test
    public void testGetVerify() {
        Story story = new Story();
        story.setVerify("1. 账号密码登录成功\n2. 手机验证码登录成功");
        assertEquals("1. 账号密码登录成功\n2. 手机验证码登录成功", story.getVerify());
    }

    @Test
    public void testGetStatus() {
        Story story = new Story();
        story.setStatus("active");
        assertEquals("active", story.getStatus());
    }

    @Test
    public void testGetStage() {
        Story story = new Story();
        story.setStage("developed");
        assertEquals("developed", story.getStage());
    }

    @Test
    public void testGetPri() {
        Story story = new Story();
        story.setPri("1");
        assertEquals("1", story.getPri());
    }

    @Test
    public void testGetSource() {
        Story story = new Story();
        story.setSource("customer");
        assertEquals("customer", story.getSource());
    }

    @Test
    public void testGetCategory() {
        Story story = new Story();
        story.setCategory("feature");
        assertEquals("feature", story.getCategory());
    }

    @Test
    public void testGetProduct() {
        Story story = new Story();
        story.setProduct(100L);
        assertEquals(Long.valueOf(100L), story.getProduct());
    }

    @Test
    public void testGetModule() {
        Story story = new Story();
        story.setModule(200L);
        assertEquals(Long.valueOf(200L), story.getModule());
    }

    @Test
    public void testGetPlan() {
        Story story = new Story();
        story.setPlan(300L);
        assertEquals(Long.valueOf(300L), story.getPlan());
    }

    @Test
    public void testGetProject() {
        Story story = new Story();
        story.setProject(400L);
        assertEquals(Long.valueOf(400L), story.getProject());
    }

    @Test
    public void testGetOpenedBy() {
        Story story = new Story();
        story.setOpenedBy("zhangsan");
        assertEquals("zhangsan", story.getOpenedBy());
    }

    @Test
    public void testGetOpenedDate() {
        Story story = new Story();
        story.setOpenedDate("2024-01-15 10:00:00");
        assertEquals("2024-01-15 10:00:00", story.getOpenedDate());
    }

    @Test
    public void testGetAssignedTo() {
        Story story = new Story();
        story.setAssignedTo("lisi");
        assertEquals("lisi", story.getAssignedTo());
    }

    @Test
    public void testGetAssignedDate() {
        Story story = new Story();
        story.setAssignedDate("2024-01-16 09:00:00");
        assertEquals("2024-01-16 09:00:00", story.getAssignedDate());
    }

    @Test
    public void testGetClosedBy() {
        Story story = new Story();
        story.setClosedBy("wangwu");
        assertEquals("wangwu", story.getClosedBy());
    }

    @Test
    public void testGetClosedDate() {
        Story story = new Story();
        story.setClosedDate("2024-01-20 17:00:00");
        assertEquals("2024-01-20 17:00:00", story.getClosedDate());
    }

    @Test
    public void testGetClosedReason() {
        Story story = new Story();
        story.setClosedReason("done");
        assertEquals("done", story.getClosedReason());
    }

    @Test
    public void testGetParent() {
        Story story = new Story();
        story.setParent(50L);
        assertEquals(Long.valueOf(50L), story.getParent());
    }

    @Test
    public void testGetParentVersion() {
        Story story = new Story();
        story.setParentVersion(1L);
        assertEquals(Long.valueOf(1L), story.getParentVersion());
    }

    @Test
    public void testGetVersion() {
        Story story = new Story();
        story.setVersion("2");
        assertEquals("2", story.getVersion());
    }

    @Test
    public void testGetDeleted() {
        Story story = new Story();
        story.setDeleted("0");
        assertEquals("0", story.getDeleted());
    }

    @Test
    public void testGetProductName() {
        Story story = new Story();
        story.setProductName("产品管理系统");
        assertEquals("产品管理系统", story.getProductName());
    }

    @Test
    public void testGetModuleName() {
        Story story = new Story();
        story.setModuleName("用户模块");
        assertEquals("用户模块", story.getModuleName());
    }

    @Test
    public void testGetProjectName() {
        Story story = new Story();
        story.setProjectName("一期项目");
        assertEquals("一期项目", story.getProjectName());
    }

    @Test
    public void testGetAttachments() {
        Story story = new Story();
        Attachment att = new Attachment();
        att.setId(1L);
        att.setTitle("doc.pdf");
        List<Attachment> attachments = Arrays.asList(att);
        story.setAttachments(attachments);
        assertEquals(1, story.getAttachments().size());
        assertEquals("doc.pdf", story.getAttachments().get(0).getTitle());
    }

    @Test
    public void testGetImageUrls() {
        Story story = new Story();
        List<String> urls = Arrays.asList("http://example.com/img1.png", "http://example.com/img2.png");
        story.setImageUrls(urls);
        assertEquals(2, story.getImageUrls().size());
    }

    @Test
    public void testNullValues() {
        Story story = new Story();
        assertNull(story.getId());
        assertNull(story.getTitle());
        assertNull(story.getSpec());
        assertNull(story.getVerify());
        assertNull(story.getStatus());
        assertNull(story.getAttachments());
    }
}