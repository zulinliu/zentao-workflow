package com.tsintergy.chandao.cli;

import org.junit.Test;

import java.util.List;

import static org.junit.Assert.*;

/**
 * CommandLineArgs 单元测试
 */
public class CommandLineArgsTest {

    @Test
    public void testIsHelp() {
        CommandLineArgs args = new CommandLineArgs();
        assertFalse(args.isHelp());
    }

    @Test
    public void testGetUrl() {
        CommandLineArgs args = new CommandLineArgs();
        assertNull(args.getUrl());
    }

    @Test
    public void testGetUsername() {
        CommandLineArgs args = new CommandLineArgs();
        assertNull(args.getUsername());
    }

    @Test
    public void testGetPassword() {
        CommandLineArgs args = new CommandLineArgs();
        assertNull(args.getPassword());
    }

    @Test
    public void testGetOutput() {
        CommandLineArgs args = new CommandLineArgs();
        assertNull(args.getOutput());
    }

    @Test
    public void testGetConfigPath() {
        CommandLineArgs args = new CommandLineArgs();
        assertNull(args.getConfigPath());
    }

    @Test
    public void testGetType() {
        CommandLineArgs args = new CommandLineArgs();
        assertEquals("story", args.getType());
    }

    @Test
    public void testGetId() {
        CommandLineArgs args = new CommandLineArgs();
        assertNull(args.getId());
    }

    @Test
    public void testGetIds() {
        CommandLineArgs args = new CommandLineArgs();
        assertNull(args.getIds());
    }

    @Test
    public void testGetProjectId() {
        CommandLineArgs args = new CommandLineArgs();
        assertNull(args.getProjectId());
    }

    @Test
    public void testIsNoAttachment() {
        CommandLineArgs args = new CommandLineArgs();
        assertFalse(args.isNoAttachment());
    }

    @Test
    public void testIsNoImage() {
        CommandLineArgs args = new CommandLineArgs();
        assertFalse(args.isNoImage());
    }

    @Test
    public void testIsVerbose() {
        CommandLineArgs args = new CommandLineArgs();
        assertFalse(args.isVerbose());
    }

    @Test
    public void testGetIdList_Empty() {
        CommandLineArgs args = new CommandLineArgs();
        List<Long> ids = args.getIdList();
        assertNotNull(ids);
        assertTrue(ids.isEmpty());
    }

    @Test
    public void testGetIdList_WithId() {
        CommandLineArgs args = new CommandLineArgs();
        try {
            java.lang.reflect.Field idField = CommandLineArgs.class.getDeclaredField("id");
            idField.setAccessible(true);
            idField.set(args, 123L);

            List<Long> ids = args.getIdList();
            assertEquals(1, ids.size());
            assertEquals(Long.valueOf(123L), ids.get(0));
        } catch (Exception e) {
            fail("Reflection failed: " + e.getMessage());
        }
    }

    @Test
    public void testGetIdList_WithIds() {
        CommandLineArgs args = new CommandLineArgs();
        try {
            java.lang.reflect.Field idsField = CommandLineArgs.class.getDeclaredField("ids");
            idsField.setAccessible(true);
            idsField.set(args, "1,2,3");

            List<Long> ids = args.getIdList();
            assertEquals(3, ids.size());
            assertEquals(Long.valueOf(1L), ids.get(0));
            assertEquals(Long.valueOf(2L), ids.get(1));
            assertEquals(Long.valueOf(3L), ids.get(2));
        } catch (Exception e) {
            fail("Reflection failed: " + e.getMessage());
        }
    }

    @Test
    public void testGetIdList_WithSpaces() {
        CommandLineArgs args = new CommandLineArgs();
        try {
            java.lang.reflect.Field idsField = CommandLineArgs.class.getDeclaredField("ids");
            idsField.setAccessible(true);
            idsField.set(args, " 1 , 2 , 3 ");

            List<Long> ids = args.getIdList();
            assertEquals(3, ids.size());
        } catch (Exception e) {
            fail("Reflection failed: " + e.getMessage());
        }
    }

    @Test
    public void testGetIdList_InvalidIdSkipped() {
        CommandLineArgs args = new CommandLineArgs();
        try {
            java.lang.reflect.Field idsField = CommandLineArgs.class.getDeclaredField("ids");
            idsField.setAccessible(true);
            idsField.set(args, "1,abc,3");

            List<Long> ids = args.getIdList();
            assertEquals(2, ids.size());
            assertEquals(Long.valueOf(1L), ids.get(0));
            assertEquals(Long.valueOf(3L), ids.get(1));
        } catch (Exception e) {
            fail("Reflection failed: " + e.getMessage());
        }
    }

    @Test
    public void testGetIdList_BothIdAndIds() {
        CommandLineArgs args = new CommandLineArgs();
        try {
            java.lang.reflect.Field idField = CommandLineArgs.class.getDeclaredField("id");
            idField.setAccessible(true);
            idField.set(args, 100L);

            java.lang.reflect.Field idsField = CommandLineArgs.class.getDeclaredField("ids");
            idsField.setAccessible(true);
            idsField.set(args, "1,2");

            List<Long> ids = args.getIdList();
            assertEquals(3, ids.size());
            assertTrue(ids.contains(1L));
            assertTrue(ids.contains(2L));
            assertTrue(ids.contains(100L));
        } catch (Exception e) {
            fail("Reflection failed: " + e.getMessage());
        }
    }

    @Test
    public void testDefaultType() {
        CommandLineArgs args = new CommandLineArgs();
        assertEquals("story", args.getType());
    }
}