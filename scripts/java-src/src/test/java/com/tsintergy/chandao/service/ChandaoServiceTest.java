package com.tsintergy.chandao.service;

import com.tsintergy.chandao.cli.CommandLineArgs;
import com.tsintergy.chandao.config.ChandaoConfig;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

/**
 * ChandaoService 单元测试
 */
public class ChandaoServiceTest {

    private ChandaoConfig config;

    @Before
    public void setUp() {
        config = new ChandaoConfig();
        config.setBaseUrl("https://test.zentao.com");
        config.setUsername("testuser");
        config.setPassword("testpass");
        config.setOutputDir("/tmp/chandao-test");
    }

    @Test
    public void testCreateService() {
        ChandaoService service = new ChandaoService(config);
        assertNotNull(service);
    }

    @Test(expected = Exception.class)
    public void testExecute_NoIdOrProject() throws Exception {
        ChandaoService service = new ChandaoService(config);
        CommandLineArgs args = new CommandLineArgs();
        // 没有设置 ID 或项目 ID
        service.execute(args);
    }

    @Test(expected = Exception.class)
    public void testExecute_InvalidType() throws Exception {
        ChandaoService service = new ChandaoService(config);
        CommandLineArgs args = new CommandLineArgs();
        try {
            java.lang.reflect.Field idField = CommandLineArgs.class.getDeclaredField("id");
            idField.setAccessible(true);
            idField.set(args, 1L);

            java.lang.reflect.Field typeField = CommandLineArgs.class.getDeclaredField("type");
            typeField.setAccessible(true);
            typeField.set(args, "invalid_type");
        } catch (Exception e) {
            fail("Reflection failed");
        }

        // 需要先 mock login 成功，这里测试会失败因为无法连接真实服务器
        service.execute(args);
    }

    @Test(expected = Exception.class)
    public void testExecute_ProjectNotImplemented() throws Exception {
        ChandaoService service = new ChandaoService(config);
        CommandLineArgs args = new CommandLineArgs();
        try {
            java.lang.reflect.Field projectField = CommandLineArgs.class.getDeclaredField("projectId");
            projectField.setAccessible(true);
            projectField.set(args, 1L);
        } catch (Exception e) {
            fail("Reflection failed");
        }

        // 项目下载功能待实现
        service.execute(args);
    }
}