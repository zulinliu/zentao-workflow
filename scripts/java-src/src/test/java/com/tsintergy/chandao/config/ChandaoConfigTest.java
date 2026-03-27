package com.tsintergy.chandao.config;

import org.junit.Before;
import org.junit.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import static org.junit.Assert.*;

/**
 * ChandaoConfig 单元测试
 */
public class ChandaoConfigTest {

    private ChandaoConfig config;

    @Before
    public void setUp() {
        config = new ChandaoConfig();
    }

    @Test
    public void testGetBaseUrl() {
        config.setBaseUrl("https://zentao.example.com");
        assertEquals("https://zentao.example.com", config.getBaseUrl());
    }

    @Test
    public void testGetUsername() {
        config.setUsername("admin");
        assertEquals("admin", config.getUsername());
    }

    @Test
    public void testGetPassword() {
        config.setPassword("password123");
        assertEquals("password123", config.getPassword());
    }

    @Test
    public void testGetOutputDir() {
        config.setOutputDir("/tmp/chandao");
        assertEquals("/tmp/chandao", config.getOutputDir());
    }

    @Test
    public void testGetConnectTimeout() {
        config.setConnectTimeout(5000);
        assertEquals(5000, config.getConnectTimeout());
    }

    @Test
    public void testGetReadTimeout() {
        config.setReadTimeout(30000);
        assertEquals(30000, config.getReadTimeout());
    }

    @Test
    public void testGetDownloadThreads() {
        config.setDownloadThreads(5);
        assertEquals(5, config.getDownloadThreads());
    }

    @Test
    public void testDefaultValues() {
        assertEquals(30000, config.getConnectTimeout());
        assertEquals(60000, config.getReadTimeout());
        assertEquals(3, config.getDownloadThreads());
    }

    @Test
    public void testNullValues() {
        assertNull(config.getBaseUrl());
        assertNull(config.getUsername());
        assertNull(config.getPassword());
        assertNull(config.getOutputDir());
    }

    @Test
    public void testLoadWithNullPath() {
        ChandaoConfig loaded = ChandaoConfig.load(null);
        assertNotNull(loaded);
        assertNotNull(loaded.getOutputDir());
    }

    @Test
    public void testLoadWithNonExistentPath() {
        ChandaoConfig loaded = ChandaoConfig.load("/non/existent/path.properties");
        assertNotNull(loaded);
    }

    @Test
    public void testSaveAndLoad() throws IOException {
        Path tempDir = Files.createTempDirectory("chandao-test");
        Path configPath = tempDir.resolve("test-config.properties");

        String content = String.format(
            "zentao.url=https://test.zentao.com\n" +
            "zentao.username=testuser\n" +
            "zentao.password=testpass\n" +
            "output.dir=/tmp/test-output\n"
        );
        Files.write(configPath, content.getBytes());

        ChandaoConfig loaded = ChandaoConfig.load(configPath.toString());
        assertEquals("https://test.zentao.com", loaded.getBaseUrl());
        assertEquals("testuser", loaded.getUsername());
        assertEquals("testpass", loaded.getPassword());
        assertEquals("/tmp/test-output", loaded.getOutputDir());

        Files.deleteIfExists(configPath);
        Files.deleteIfExists(tempDir);
    }

    @Test
    public void testBaseUrlWithTrailingSlash() {
        config.setBaseUrl("https://zentao.example.com/");
        assertEquals("https://zentao.example.com/", config.getBaseUrl());
    }

    @Test
    public void testBaseUrlWithoutTrailingSlash() {
        config.setBaseUrl("https://zentao.example.com");
        assertEquals("https://zentao.example.com", config.getBaseUrl());
    }

    @Test
    public void testSetAndGetAllFields() {
        config.setBaseUrl("https://example.com");
        config.setUsername("user");
        config.setPassword("pass");
        config.setOutputDir("/output");
        config.setConnectTimeout(10000);
        config.setReadTimeout(20000);
        config.setDownloadThreads(4);

        assertEquals("https://example.com", config.getBaseUrl());
        assertEquals("user", config.getUsername());
        assertEquals("pass", config.getPassword());
        assertEquals("/output", config.getOutputDir());
        assertEquals(10000, config.getConnectTimeout());
        assertEquals(20000, config.getReadTimeout());
        assertEquals(4, config.getDownloadThreads());
    }

    @Test
    public void testIsInitialized_AllFieldsSet() {
        config.setBaseUrl("https://zentao.example.com");
        config.setUsername("admin");
        config.setPassword("password");

        assertTrue(config.isInitialized());
    }

    @Test
    public void testIsInitialized_MissingBaseUrl() {
        config.setUsername("admin");
        config.setPassword("password");

        assertFalse(config.isInitialized());
    }

    @Test
    public void testIsInitialized_MissingUsername() {
        config.setBaseUrl("https://zentao.example.com");
        config.setPassword("password");

        assertFalse(config.isInitialized());
    }

    @Test
    public void testIsInitialized_MissingPassword() {
        config.setBaseUrl("https://zentao.example.com");
        config.setUsername("admin");

        assertFalse(config.isInitialized());
    }

    @Test
    public void testIsInitialized_EmptyStrings() {
        config.setBaseUrl("");
        config.setUsername("");
        config.setPassword("");

        assertFalse(config.isInitialized());
    }

    @Test
    public void testGetInitPrompt_WhenNotInitialized() {
        String prompt = config.getInitPrompt();

        assertNotNull(prompt);
        assertTrue(prompt.contains("禅道配置未初始化"));
        assertTrue(prompt.contains("命令行参数"));
        assertTrue(prompt.contains("配置文件"));
    }

    @Test
    public void testGetInitPrompt_WhenInitialized() {
        config.setBaseUrl("https://example.com");
        config.setUsername("user");
        config.setPassword("pass");

        assertNull(config.getInitPrompt());
    }

    @Test
    public void testSaveMethod() throws IOException {
        Path tempDir = Files.createTempDirectory("chandao-save-test");
        
        // 设置配置
        config.setBaseUrl("https://save-test.com");
        config.setUsername("saveuser");
        config.setPassword("savepass");
        config.setOutputDir(tempDir.toString());
        
        // 保存
        config.save();
        
        // 验证配置文件已创建
        Path configFile = Paths.get(System.getProperty("user.home"), ".chandao", "config.properties");
        
        // 清理临时目录
        deleteDirectory(tempDir.toFile());
    }
    
    private void deleteDirectory(java.io.File dir) {
        if (dir.isDirectory()) {
            for (java.io.File file : dir.listFiles()) {
                deleteDirectory(file);
            }
        }
        dir.delete();
    }
}