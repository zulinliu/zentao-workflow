package com.tsintergy.chandao.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Properties;

/**
 * 禅道配置
 */
public class ChandaoConfig {
    
    private static final Logger log = LoggerFactory.getLogger(ChandaoConfig.class);
    
    private String baseUrl;
    private String username;
    private String password;
    private String outputDir;
    private int connectTimeout = 30000;
    private int readTimeout = 60000;
    private int downloadThreads = 3;
    
    // 默认配置文件路径
    private static final String DEFAULT_CONFIG_FILE = ".chandao/config.properties";
    
    public static ChandaoConfig load(String configPath) {
        ChandaoConfig config = new ChandaoConfig();
        
        // 尝试加载配置文件
        Path path = getConfigPath(configPath);
        if (path != null && Files.exists(path)) {
            try (InputStream is = Files.newInputStream(path)) {
                Properties props = new Properties();
                props.load(is);
                
                config.baseUrl = props.getProperty("zentao.url", config.baseUrl);
                config.username = props.getProperty("zentao.username", config.username);
                config.password = props.getProperty("zentao.password", config.password);
                config.outputDir = props.getProperty("output.dir", config.outputDir);
                
                log.info("已加载配置文件: {}", path);
            } catch (IOException e) {
                log.warn("加载配置文件失败: {}", e.getMessage());
            }
        }
        
        // 设置默认输出目录
        if (config.outputDir == null || config.outputDir.isEmpty()) {
            config.outputDir = System.getProperty("user.home") + "/chandao";
        }
        
        return config;
    }
    
    private static Path getConfigPath(String configPath) {
        if (configPath != null && !configPath.isEmpty()) {
            return Paths.get(configPath);
        }
        return Paths.get(System.getProperty("user.home"), DEFAULT_CONFIG_FILE);
    }
    
    /**
     * 保存配置到文件
     */
    public void save() {
        Path path = Paths.get(System.getProperty("user.home"), DEFAULT_CONFIG_FILE);
        try {
            Files.createDirectories(path.getParent());
            Properties props = new Properties();
            if (baseUrl != null) props.setProperty("zentao.url", baseUrl);
            if (username != null) props.setProperty("zentao.username", username);
            if (password != null) props.setProperty("zentao.password", password);
            if (outputDir != null) props.setProperty("output.dir", outputDir);
            
            try (OutputStream os = Files.newOutputStream(path)) {
                props.store(os, "Chandao Fetch Configuration");
            }
            log.info("配置已保存到: {}", path);
        } catch (IOException e) {
            log.error("保存配置失败: {}", e.getMessage());
        }
    }
    
    /**
     * 检查配置是否已初始化
     */
    public boolean isInitialized() {
        return baseUrl != null && !baseUrl.isEmpty()
            && username != null && !username.isEmpty()
            && password != null && !password.isEmpty();
    }
    
    /**
     * 获取初始化提示信息
     */
    public String getInitPrompt() {
        if (isInitialized()) {
            return null;
        }
        StringBuilder sb = new StringBuilder();
        sb.append("禅道配置未初始化！请通过以下方式之一提供配置：\n\n");
        sb.append("方式一：命令行参数\n");
        sb.append("  java -jar chandao-fetch.jar --url <禅道地址> --username <用户名> --password <密码>\n\n");
        sb.append("方式二：配置文件\n");
        sb.append("  在用户目录创建 ~/.chandao/config.properties 文件：\n");
        sb.append("  zentao.url=https://your-zentao-server.com\n");
        sb.append("  zentao.username=your_username\n");
        sb.append("  zentao.password=your_password\n\n");
        sb.append("首次配置后，配置将自动保存到 ~/.chandao/config.properties");
        return sb.toString();
    }
    
    // Getters and Setters
    public String getBaseUrl() { return baseUrl; }
    public void setBaseUrl(String baseUrl) { this.baseUrl = baseUrl; }
    
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    
    public String getOutputDir() { return outputDir; }
    public void setOutputDir(String outputDir) { this.outputDir = outputDir; }
    
    public int getConnectTimeout() { return connectTimeout; }
    public void setConnectTimeout(int connectTimeout) { this.connectTimeout = connectTimeout; }
    
    public int getReadTimeout() { return readTimeout; }
    public void setReadTimeout(int readTimeout) { this.readTimeout = readTimeout; }
    
    public int getDownloadThreads() { return downloadThreads; }
    public void setDownloadThreads(int downloadThreads) { this.downloadThreads = downloadThreads; }
}