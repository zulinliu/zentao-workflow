package com.tsintergy.chandao;

import com.beust.jcommander.JCommander;
import com.tsintergy.chandao.cli.CommandLineArgs;
import com.tsintergy.chandao.config.ChandaoConfig;
import com.tsintergy.chandao.service.ChandaoService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 禅道数据抓取工具主入口
 */
public class ChandaoFetchApplication {
    
    private static final Logger log = LoggerFactory.getLogger(ChandaoFetchApplication.class);
    
    public static void main(String[] args) {
        CommandLineArgs cliArgs = new CommandLineArgs();
        JCommander commander = JCommander.newBuilder()
                .addObject(cliArgs)
                .build();
        
        try {
            commander.parse(args);
            
            if (cliArgs.isHelp()) {
                commander.usage();
                return;
            }
            
            // 加载配置
            ChandaoConfig config = ChandaoConfig.load(cliArgs.getConfigPath());
            
            // 命令行参数覆盖配置文件
            if (cliArgs.getUrl() != null) {
                config.setBaseUrl(cliArgs.getUrl());
            }
            if (cliArgs.getUsername() != null) {
                config.setUsername(cliArgs.getUsername());
            }
            if (cliArgs.getPassword() != null) {
                config.setPassword(cliArgs.getPassword());
            }
            if (cliArgs.getOutput() != null) {
                config.setOutputDir(cliArgs.getOutput());
            }
            
            // 检查配置是否已初始化
            if (!config.isInitialized()) {
                System.err.println(config.getInitPrompt());
                System.exit(1);
            }
            
            // 如果提供了新的凭据，自动保存配置
            if (cliArgs.getUrl() != null || cliArgs.getUsername() != null || cliArgs.getPassword() != null) {
                config.save();
                log.info("配置已自动保存到 ~/.chandao/config.properties");
            }
            
            // 执行服务
            ChandaoService service = new ChandaoService(config);
            service.execute(cliArgs);
            
            log.info("任务执行完成");
            
        } catch (Exception e) {
            log.error("执行失败: {}", e.getMessage(), e);
            System.exit(1);
        }
    }
}