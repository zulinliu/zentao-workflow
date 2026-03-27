package com.tsintergy.chandao.model;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Attachment 单元测试
 */
public class AttachmentTest {

    @Test
    public void testGetId() {
        Attachment att = new Attachment();
        att.setId(123L);
        assertEquals(Long.valueOf(123L), att.getId());
    }

    @Test
    public void testGetTitle() {
        Attachment att = new Attachment();
        att.setTitle("test.pdf");
        assertEquals("test.pdf", att.getTitle());
    }

    @Test
    public void testGetPathname() {
        Attachment att = new Attachment();
        att.setPathname("/data/upload/202401/test.pdf");
        assertEquals("/data/upload/202401/test.pdf", att.getPathname());
    }

    @Test
    public void testGetExtension() {
        Attachment att = new Attachment();
        att.setExtension("pdf");
        assertEquals("pdf", att.getExtension());
    }

    @Test
    public void testGetSize() {
        Attachment att = new Attachment();
        att.setSize(1024L);
        assertEquals(Long.valueOf(1024L), att.getSize());
    }

    @Test
    public void testGetObjectType() {
        Attachment att = new Attachment();
        att.setObjectType("story");
        assertEquals("story", att.getObjectType());
    }

    @Test
    public void testGetObjectId() {
        Attachment att = new Attachment();
        att.setObjectId(456L);
        assertEquals(Long.valueOf(456L), att.getObjectId());
    }

    @Test
    public void testGetAddedBy() {
        Attachment att = new Attachment();
        att.setAddedBy("admin");
        assertEquals("admin", att.getAddedBy());
    }

    @Test
    public void testGetAddedDate() {
        Attachment att = new Attachment();
        att.setAddedDate("2024-01-15 10:30:00");
        assertEquals("2024-01-15 10:30:00", att.getAddedDate());
    }

    @Test
    public void testGetDownloads() {
        Attachment att = new Attachment();
        att.setDownloads("5");
        assertEquals("5", att.getDownloads());
    }

    @Test
    public void testGetLocalPath() {
        Attachment att = new Attachment();
        att.setLocalPath("/tmp/download/test.pdf");
        assertEquals("/tmp/download/test.pdf", att.getLocalPath());
    }

    @Test
    public void testIsImage_Jpg() {
        Attachment att = new Attachment();
        att.setExtension("jpg");
        assertTrue(att.isImage());
    }

    @Test
    public void testIsImage_Jpeg() {
        Attachment att = new Attachment();
        att.setExtension("jpeg");
        assertTrue(att.isImage());
    }

    @Test
    public void testIsImage_Png() {
        Attachment att = new Attachment();
        att.setExtension("png");
        assertTrue(att.isImage());
    }

    @Test
    public void testIsImage_Gif() {
        Attachment att = new Attachment();
        att.setExtension("gif");
        assertTrue(att.isImage());
    }

    @Test
    public void testIsImage_Bmp() {
        Attachment att = new Attachment();
        att.setExtension("bmp");
        assertTrue(att.isImage());
    }

    @Test
    public void testIsImage_Webp() {
        Attachment att = new Attachment();
        att.setExtension("webp");
        assertTrue(att.isImage());
    }

    @Test
    public void testIsImage_Uppercase() {
        Attachment att = new Attachment();
        att.setExtension("PNG");
        assertTrue(att.isImage());
    }

    @Test
    public void testIsImage_NonImage() {
        Attachment att = new Attachment();
        att.setExtension("pdf");
        assertFalse(att.isImage());
    }

    @Test
    public void testIsImage_NullExtension() {
        Attachment att = new Attachment();
        assertFalse(att.isImage());
    }

    @Test
    public void testGetFileName_WithTitle() {
        Attachment att = new Attachment();
        att.setTitle("document.pdf");
        assertEquals("document.pdf", att.getFileName());
    }

    @Test
    public void testGetFileName_WithPathname() {
        Attachment att = new Attachment();
        att.setPathname("/data/upload/202401/report.pdf");
        assertEquals("report.pdf", att.getFileName());
    }

    @Test
    public void testGetFileName_WithPathnameNoSlash() {
        Attachment att = new Attachment();
        att.setPathname("report.pdf");
        assertEquals("report.pdf", att.getFileName());
    }

    @Test
    public void testGetFileName_WithIdFallback() {
        Attachment att = new Attachment();
        att.setId(789L);
        assertEquals("attachment_789", att.getFileName());
    }

    @Test
    public void testGetFileName_TitleTakesPrecedence() {
        Attachment att = new Attachment();
        att.setTitle("custom_name.pdf");
        att.setPathname("/data/upload/202401/original.pdf");
        assertEquals("custom_name.pdf", att.getFileName());
    }
}