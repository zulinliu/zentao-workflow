package com.tsintergy.chandao.cli;

import com.beust.jcommander.Parameter;

import java.util.ArrayList;
import java.util.List;

/**
 * 命令行参数定义
 */
public class CommandLineArgs {
    
    @Parameter(names = {"-h", "--help"}, description = "显示帮助信息", help = true)
    private boolean help;
    
    @Parameter(names = {"-u", "--url"}, description = "禅道地址，如 https://zentao.example.com")
    private String url;
    
    @Parameter(names = {"--username"}, description = "用户名")
    private String username;
    
    @Parameter(names = {"--password"}, description = "密码")
    private String password;
    
    @Parameter(names = {"-o", "--output"}, description = "输出目录，默认 ~/chandao")
    private String output;
    
    @Parameter(names = {"-c", "--config"}, description = "配置文件路径")
    private String configPath;
    
    @Parameter(names = {"-t", "--type"}, description = "数据类型: story/task/bug/all")
    private String type = "story";
    
    @Parameter(names = {"-i", "--id"}, description = "单个ID下载")
    private Long id;
    
    @Parameter(names = {"--ids"}, description = "批量ID下载，逗号分隔")
    private String ids;
    
    @Parameter(names = {"-p", "--project"}, description = "项目ID，下载整个项目")
    private Long projectId;
    
    @Parameter(names = {"--no-attachment"}, description = "不下载附件")
    private boolean noAttachment = false;
    
    @Parameter(names = {"--no-image"}, description = "不下载图片")
    private boolean noImage = false;
    
    @Parameter(names = {"-v", "--verbose"}, description = "详细输出")
    private boolean verbose = false;
    
    // Getters
    public boolean isHelp() { return help; }
    public String getUrl() { return url; }
    public String getUsername() { return username; }
    public String getPassword() { return password; }
    public String getOutput() { return output; }
    public String getConfigPath() { return configPath; }
    public String getType() { return type; }
    public Long getId() { return id; }
    public String getIds() { return ids; }
    public Long getProjectId() { return projectId; }
    public boolean isNoAttachment() { return noAttachment; }
    public boolean isNoImage() { return noImage; }
    public boolean isVerbose() { return verbose; }
    
    /**
     * 获取ID列表
     */
    public List<Long> getIdList() {
        List<Long> result = new ArrayList<>();
        if (ids != null && !ids.isEmpty()) {
            for (String s : ids.split(",")) {
                try {
                    result.add(Long.parseLong(s.trim()));
                } catch (NumberFormatException e) {
                    // skip invalid
                }
            }
        }
        if (id != null) {
            result.add(id);
        }
        return result;
    }
}