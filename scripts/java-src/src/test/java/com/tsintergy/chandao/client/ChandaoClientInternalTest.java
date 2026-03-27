package com.tsintergy.chandao.client;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.tsintergy.chandao.config.ChandaoConfig;
import com.tsintergy.chandao.model.Attachment;
import org.junit.Test;

import java.lang.reflect.Method;
import java.util.List;

import static org.junit.Assert.*;

/**
 * ChandaoClient additional tests for internal methods
 */
public class ChandaoClientInternalTest {

    @Test
    public void testParseAttachments_Null() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode nullNode = null;
        
        ChandaoConfig config = new ChandaoConfig();
        config.setBaseUrl("http://test.com");
        ChandaoClient client = new ChandaoClient(config);
        
        Method method = ChandaoClient.class.getDeclaredMethod("parseAttachments", JsonNode.class);
        method.setAccessible(true);
        
        @SuppressWarnings("unchecked")
        List<Attachment> result = (List<Attachment>) method.invoke(client, nullNode);
        
        assertNotNull(result);
        assertTrue(result.isEmpty());
    }

    @Test
    public void testParseAttachments_EmptyObject() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode emptyNode = mapper.readTree("{}");
        
        ChandaoConfig config = new ChandaoConfig();
        config.setBaseUrl("http://test.com");
        ChandaoClient client = new ChandaoClient(config);
        
        Method method = ChandaoClient.class.getDeclaredMethod("parseAttachments", JsonNode.class);
        method.setAccessible(true);
        
        @SuppressWarnings("unchecked")
        List<Attachment> result = (List<Attachment>) method.invoke(client, emptyNode);
        
        assertNotNull(result);
        assertTrue(result.isEmpty());
    }

    @Test
    public void testParseAttachments_ValidFiles() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode filesNode = mapper.readTree("{\"1\":{\"id\":1,\"title\":\"doc.pdf\",\"extension\":\"pdf\"}}");
        
        ChandaoConfig config = new ChandaoConfig();
        config.setBaseUrl("http://test.com");
        ChandaoClient client = new ChandaoClient(config);
        
        Method method = ChandaoClient.class.getDeclaredMethod("parseAttachments", JsonNode.class);
        method.setAccessible(true);
        
        @SuppressWarnings("unchecked")
        List<Attachment> result = (List<Attachment>) method.invoke(client, filesNode);
        
        assertNotNull(result);
        assertEquals(1, result.size());
        assertEquals("doc.pdf", result.get(0).getTitle());
    }

    @Test
    public void testParseAttachments_MultipleFiles() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode filesNode = mapper.readTree(
            "{\"1\":{\"id\":1,\"title\":\"a.pdf\",\"extension\":\"pdf\"}," +
            "\"2\":{\"id\":2,\"title\":\"b.png\",\"extension\":\"png\"}}"
        );
        
        ChandaoConfig config = new ChandaoConfig();
        config.setBaseUrl("http://test.com");
        ChandaoClient client = new ChandaoClient(config);
        
        Method method = ChandaoClient.class.getDeclaredMethod("parseAttachments", JsonNode.class);
        method.setAccessible(true);
        
        @SuppressWarnings("unchecked")
        List<Attachment> result = (List<Attachment>) method.invoke(client, filesNode);
        
        assertNotNull(result);
        assertEquals(2, result.size());
    }

    @Test
    public void testParseAttachments_InvalidEntry() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        // 包含无效数据的条目应该被跳过
        JsonNode filesNode = mapper.readTree(
            "{\"1\":{\"id\":1,\"title\":\"valid.pdf\"},\"2\":\"invalid_string\"}"
        );
        
        ChandaoConfig config = new ChandaoConfig();
        config.setBaseUrl("http://test.com");
        ChandaoClient client = new ChandaoClient(config);
        
        Method method = ChandaoClient.class.getDeclaredMethod("parseAttachments", JsonNode.class);
        method.setAccessible(true);
        
        @SuppressWarnings("unchecked")
        List<Attachment> result = (List<Attachment>) method.invoke(client, filesNode);
        
        assertNotNull(result);
        // 至少有一个有效条目
        assertTrue(result.size() >= 1);
    }

    @Test
    public void testParseAttachments_ArrayNode() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        // 数组格式也应该返回空列表（期望对象格式）
        JsonNode arrayNode = mapper.readTree("[{\"id\":1}]");
        
        ChandaoConfig config = new ChandaoConfig();
        config.setBaseUrl("http://test.com");
        ChandaoClient client = new ChandaoClient(config);
        
        Method method = ChandaoClient.class.getDeclaredMethod("parseAttachments", JsonNode.class);
        method.setAccessible(true);
        
        @SuppressWarnings("unchecked")
        List<Attachment> result = (List<Attachment>) method.invoke(client, arrayNode);
        
        assertNotNull(result);
        assertTrue(result.isEmpty());
    }
}