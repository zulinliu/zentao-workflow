package com.tsintergy.chandao.service;

import org.junit.Test;

import java.lang.reflect.Method;

import static org.junit.Assert.*;

/**
 * MarkdownExporter additional tests for edge cases
 */
public class MarkdownExporterEdgeCaseTest {

    @Test
    public void testProcessContent_Null() throws Exception {
        MarkdownExporter exporter = new MarkdownExporter("/tmp");
        Method method = MarkdownExporter.class.getDeclaredMethod("processContent", String.class);
        method.setAccessible(true);
        
        String result = (String) method.invoke(exporter, (String) null);
        assertEquals("", result);
    }

    @Test
    public void testProcessContent_Empty() throws Exception {
        MarkdownExporter exporter = new MarkdownExporter("/tmp");
        Method method = MarkdownExporter.class.getDeclaredMethod("processContent", String.class);
        method.setAccessible(true);
        
        String result = (String) method.invoke(exporter, "");
        assertEquals("", result);
    }

    @Test
    public void testProcessContent_NoImages() throws Exception {
        MarkdownExporter exporter = new MarkdownExporter("/tmp");
        Method method = MarkdownExporter.class.getDeclaredMethod("processContent", String.class);
        method.setAccessible(true);
        
        String result = (String) method.invoke(exporter, "Just plain text without images");
        assertEquals("Just plain text without images", result);
    }

    @Test
    public void testProcessContent_SingleImage() throws Exception {
        MarkdownExporter exporter = new MarkdownExporter("/tmp");
        Method method = MarkdownExporter.class.getDeclaredMethod("processContent", String.class);
        method.setAccessible(true);
        
        String result = (String) method.invoke(exporter, "Text <img src=\"data/upload/test.png\" /> more text");
        assertTrue(result.contains("![](attachments/test.png)"));
    }

    @Test
    public void testProcessContent_ImageWithFullPath() throws Exception {
        MarkdownExporter exporter = new MarkdownExporter("/tmp");
        Method method = MarkdownExporter.class.getDeclaredMethod("processContent", String.class);
        method.setAccessible(true);
        
        String result = (String) method.invoke(exporter, "<img src=\"/var/www/html/data/upload/2024/image.jpg\" />");
        assertTrue(result.contains("![](attachments/image.jpg)"));
    }

    @Test
    public void testProcessContent_ImageWithAttributes() throws Exception {
        MarkdownExporter exporter = new MarkdownExporter("/tmp");
        Method method = MarkdownExporter.class.getDeclaredMethod("processContent", String.class);
        method.setAccessible(true);
        
        String result = (String) method.invoke(exporter, "<img alt=\"描述\" src=\"pic.png\" width=\"100\" />");
        assertTrue(result.contains("![](attachments/pic.png)"));
    }

    @Test
    public void testNullSafe_Null() throws Exception {
        MarkdownExporter exporter = new MarkdownExporter("/tmp");
        Method method = MarkdownExporter.class.getDeclaredMethod("nullSafe", String.class);
        method.setAccessible(true);
        
        String result = (String) method.invoke(exporter, (String) null);
        assertEquals("-", result);
    }

    @Test
    public void testNullSafe_NonNull() throws Exception {
        MarkdownExporter exporter = new MarkdownExporter("/tmp");
        Method method = MarkdownExporter.class.getDeclaredMethod("nullSafe", String.class);
        method.setAccessible(true);
        
        String result = (String) method.invoke(exporter, "test value");
        assertEquals("test value", result);
    }

    @Test
    public void testNullSafe_Empty() throws Exception {
        MarkdownExporter exporter = new MarkdownExporter("/tmp");
        Method method = MarkdownExporter.class.getDeclaredMethod("nullSafe", String.class);
        method.setAccessible(true);
        
        String result = (String) method.invoke(exporter, "");
        assertEquals("", result);
    }
}