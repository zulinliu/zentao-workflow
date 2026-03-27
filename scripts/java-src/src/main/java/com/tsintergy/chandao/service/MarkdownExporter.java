package com.tsintergy.chandao.service;

import com.tsintergy.chandao.model.Attachment;
import com.tsintergy.chandao.model.Story;
import com.tsintergy.chandao.model.Task;
import com.tsintergy.chandao.model.Bug;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Markdown导出服务
 */
public class MarkdownExporter {

    private static final Logger log = LoggerFactory.getLogger(MarkdownExporter.class);

    private final String outputDir;

    public MarkdownExporter(String outputDir) {
        this.outputDir = outputDir;
    }

    /**
     * 导出需求
     */
    public void exportStory(Story story) throws IOException {
        StringBuilder md = new StringBuilder();

        String safeTitle = sanitizeFileName(story.getTitle());
        String fileName = story.getId() + "-" + safeTitle;
        String attachPath = "../attachments/story/" + story.getId();

        md.append("# 【").append(story.getTitle()).append("】").append(story.getId()).append("\n\n");
        md.append("> 类型: 需求\n\n");

        // 基本信息
        md.append("## 基本信息\n\n");
        md.append("| 字段 | 值 |\n");
        md.append("|------|----|\n");
        md.append("| 状态 | ").append(nullSafe(story.getStatus())).append(" |\n");
        md.append("| 阶段 | ").append(nullSafe(story.getStage())).append(" |\n");
        md.append("| 优先级 | ").append(nullSafe(story.getPri())).append(" |\n");
        md.append("| 来源 | ").append(nullSafe(story.getSource())).append(" |\n");
        md.append("| 分类 | ").append(nullSafe(story.getCategory())).append(" |\n");
        if (story.getProductName() != null) {
            md.append("| 产品 | ").append(story.getProductName()).append(" |\n");
        }
        if (story.getProjectName() != null) {
            md.append("| 项目 | ").append(story.getProjectName()).append(" |\n");
        }
        md.append("| 创建人 | ").append(nullSafe(story.getOpenedBy())).append(" |\n");
        md.append("| 创建时间 | ").append(nullSafe(story.getOpenedDate())).append(" |\n");
        md.append("| 指派给 | ").append(nullSafe(story.getAssignedTo())).append(" |\n");
        md.append("\n");

        // 需求描述
        if (story.getSpec() != null && !story.getSpec().isEmpty()) {
            md.append("## 需求描述\n\n");
            md.append(processContent(story.getSpec(), attachPath)).append("\n\n");
        }

        // 验收标准
        if (story.getVerify() != null && !story.getVerify().isEmpty()) {
            md.append("## 验收标准\n\n");
            md.append(processContent(story.getVerify(), attachPath)).append("\n\n");
        }

        // 附件
        appendAttachments(md, story.getAttachments(), attachPath);

        // 写入文件
        Path filePath = Paths.get(outputDir, "story", fileName + ".md");
        writeFile(filePath, md.toString());

        log.info("导出需求: {}", filePath);
    }

    /**
     * 导出任务
     */
    public void exportTask(Task task) throws IOException {
        StringBuilder md = new StringBuilder();

        String safeName = sanitizeFileName(task.getName());
        String fileName = task.getId() + "-" + safeName;
        String attachPath = "../attachments/task/" + task.getId();

        md.append("# 【").append(task.getName()).append("】").append(task.getId()).append("\n\n");
        md.append("> 类型: 任务\n\n");

        // 基本信息
        md.append("## 基本信息\n\n");
        md.append("| 字段 | 值 |\n");
        md.append("|------|----|\n");
        md.append("| 状态 | ").append(nullSafe(task.getStatus())).append(" |\n");
        md.append("| 类型 | ").append(nullSafe(task.getType())).append(" |\n");
        md.append("| 优先级 | ").append(nullSafe(task.getPri())).append(" |\n");
        if (task.getProjectName() != null) {
            md.append("| 项目 | ").append(task.getProjectName()).append(" |\n");
        }
        if (task.getStoryTitle() != null) {
            md.append("| 相关需求 | ").append(task.getStoryTitle()).append(" |\n");
        }
        md.append("| 创建人 | ").append(nullSafe(task.getOpenedBy())).append(" |\n");
        md.append("| 创建时间 | ").append(nullSafe(task.getOpenedDate())).append(" |\n");
        md.append("| 指派给 | ").append(nullSafe(task.getAssignedTo())).append(" |\n");
        if (task.getDeadline() != null) {
            md.append("| 截止日期 | ").append(task.getDeadline()).append(" |\n");
        }
        if (task.getEstimate() != null) {
            md.append("| 预计工时 | ").append(task.getEstimate()).append("h |\n");
        }
        if (task.getConsumed() != null) {
            md.append("| 已消耗 | ").append(task.getConsumed()).append("h |\n");
        }
        md.append("\n");

        // 任务描述
        if (task.getDesc() != null && !task.getDesc().isEmpty()) {
            md.append("## 任务描述\n\n");
            md.append(processContent(task.getDesc(), attachPath)).append("\n\n");
        }

        // 附件
        appendAttachments(md, task.getAttachments(), attachPath);

        // 写入文件
        Path filePath = Paths.get(outputDir, "task", fileName + ".md");
        writeFile(filePath, md.toString());

        log.info("导出任务: {}", filePath);
    }

    /**
     * 导出Bug
     */
    public void exportBug(Bug bug) throws IOException {
        StringBuilder md = new StringBuilder();

        String safeTitle = sanitizeFileName(bug.getTitle());
        String fileName = bug.getId() + "-" + safeTitle;
        String attachPath = "../attachments/bug/" + bug.getId();

        md.append("# 【").append(bug.getTitle()).append("】").append(bug.getId()).append("\n\n");
        md.append("> 类型: Bug\n\n");

        // 基本信息
        md.append("## 基本信息\n\n");
        md.append("| 字段 | 值 |\n");
        md.append("|------|----|\n");
        md.append("| 状态 | ").append(nullSafe(bug.getStatus())).append(" |\n");
        md.append("| 严重程度 | ").append(nullSafe(bug.getSeverity())).append(" |\n");
        md.append("| 优先级 | ").append(nullSafe(bug.getPri())).append(" |\n");
        md.append("| 类型 | ").append(nullSafe(bug.getType())).append(" |\n");
        if (bug.getProductName() != null) {
            md.append("| 产品 | ").append(bug.getProductName()).append(" |\n");
        }
        if (bug.getProjectName() != null) {
            md.append("| 项目 | ").append(bug.getProjectName()).append(" |\n");
        }
        md.append("| 创建人 | ").append(nullSafe(bug.getOpenedBy())).append(" |\n");
        md.append("| 创建时间 | ").append(nullSafe(bug.getOpenedDate())).append(" |\n");
        md.append("| 指派给 | ").append(nullSafe(bug.getAssignedTo())).append(" |\n");
        if (bug.getResolvedBy() != null) {
            md.append("| 解决人 | ").append(bug.getResolvedBy()).append(" |\n");
            md.append("| 解决时间 | ").append(nullSafe(bug.getResolvedDate())).append(" |\n");
            md.append("| 解决方案 | ").append(nullSafe(bug.getResolution())).append(" |\n");
        }
        md.append("\n");

        // 重现步骤
        if (bug.getSteps() != null && !bug.getSteps().isEmpty()) {
            md.append("## 重现步骤\n\n");
            md.append(processContent(bug.getSteps(), attachPath)).append("\n\n");
        }

        // 附件
        appendAttachments(md, bug.getAttachments(), attachPath);

        // 写入文件
        Path filePath = Paths.get(outputDir, "bug", fileName + ".md");
        writeFile(filePath, md.toString());

        log.info("导出Bug: {}", filePath);
    }

    /**
     * 处理内容：将 HTML 转换为 Markdown
     * @param content 原始内容（可能包含 HTML 标签）
     * @param attachPath 附件相对路径 (如 ../attachments/bug/66445)
     */
    private String processContent(String content, String attachPath) {
        if (content == null) return "";

        String result = content;

        // 1. 先处理图片标签（在 HTML 转换之前）
        result = convertImgTags(result, attachPath);

        // 2. HTML 转 Markdown
        result = htmlToMarkdown(result);

        // 3. 清理多余的空行
        result = result.replaceAll("\n{3,}", "\n\n").trim();

        return result;
    }

    /**
     * 将 HTML 转换为 Markdown
     */
    private String htmlToMarkdown(String html) {
        if (html == null) return "";

        String result = html;

        // 标题转换 (h1-h6)
        result = result.replaceAll("(?i)<h1[^>]*>\\s*", "\n\n# ");
        result = result.replaceAll("(?i)<h2[^>]*>\\s*", "\n\n## ");
        result = result.replaceAll("(?i)<h3[^>]*>\\s*", "\n\n### ");
        result = result.replaceAll("(?i)<h4[^>]*>\\s*", "\n\n#### ");
        result = result.replaceAll("(?i)<h5[^>]*>\\s*", "\n\n##### ");
        result = result.replaceAll("(?i)<h6[^>]*>\\s*", "\n\n###### ");
        result = result.replaceAll("(?i)</h[1-6]>", "\n\n");

        // 段落
        result = result.replaceAll("(?i)<p[^>]*>\\s*", "\n\n");
        result = result.replaceAll("(?i)</p>", "\n\n");

        // 换行
        result = result.replaceAll("(?i)<br\\s*/?>\\s*", "\n");
        result = result.replaceAll("(?i)<br[^>]*>", "\n");

        // 列表
        result = result.replaceAll("(?i)<ul[^>]*>\\s*", "\n");
        result = result.replaceAll("(?i)</ul>", "\n");
        result = result.replaceAll("(?i)<ol[^>]*>\\s*", "\n");
        result = result.replaceAll("(?i)</ol>", "\n");
        result = result.replaceAll("(?i)<li[^>]*>\\s*", "- ");
        result = result.replaceAll("(?i)</li>", "\n");

        // 有序列表项（保留 ol 中的数字）
        // 这个需要在处理完 ul 后单独处理

        // 强调和粗体
        result = result.replaceAll("(?i)<strong[^>]*>\\s*", "**");
        result = result.replaceAll("(?i)</strong>", "**");
        result = result.replaceAll("(?i)<b[^>]*>\\s*", "**");
        result = result.replaceAll("(?i)</b>", "**");
        result = result.replaceAll("(?i)<em[^>]*>\\s*", "*");
        result = result.replaceAll("(?i)</em>", "*");
        result = result.replaceAll("(?i)<i[^>]*>\\s*", "*");
        result = result.replaceAll("(?i)</i>", "*");

        // 代码
        result = result.replaceAll("(?i)<code[^>]*>\\s*", "`");
        result = result.replaceAll("(?i)</code>", "`");
        result = result.replaceAll("(?i)<pre[^>]*>\\s*", "\n\n```\n");
        result = result.replaceAll("(?i)</pre>", "\n```\n\n");

        // 链接
        result = result.replaceAll("(?i)<a[^>]+href=\"([^\"]+)\"[^>]*>\\s*([^<]*)</a>", "[$2]($1)");

        // 引用
        result = result.replaceAll("(?i)<blockquote[^>]*>\\s*", "\n\n> ");
        result = result.replaceAll("(?i)</blockquote>", "\n\n");

        // 分隔线
        result = result.replaceAll("(?i)<hr\\s*/?>\\s*", "\n\n---\n\n");
        result = result.replaceAll("(?i)<hr[^>]*>", "\n\n---\n\n");

        // 表格相关（简化处理）
        result = result.replaceAll("(?i)<table[^>]*>\\s*", "\n\n");
        result = result.replaceAll("(?i)</table>", "\n\n");
        result = result.replaceAll("(?i)<tr[^>]*>\\s*", "| ");
        result = result.replaceAll("(?i)</tr>", " |\n");
        result = result.replaceAll("(?i)<td[^>]*>\\s*", " ");
        result = result.replaceAll("(?i)</td>", " |");
        result = result.replaceAll("(?i)<th[^>]*>\\s*", " ");
        result = result.replaceAll("(?i)</th>", " |");
        result = result.replaceAll("(?i)<thead[^>]*>\\s*", "");
        result = result.replaceAll("(?i)</thead>", "");
        result = result.replaceAll("(?i)<tbody[^>]*>\\s*", "");
        result = result.replaceAll("(?i)</tbody>", "");

        // Span 和 div（移除标签，保留内容）
        result = result.replaceAll("(?i)<span[^>]*>", "");
        result = result.replaceAll("(?i)</span>", "");
        result = result.replaceAll("(?i)<div[^>]*>\\s*", "\n");
        result = result.replaceAll("(?i)</div>", "\n");

        // 移除其他未知标签，保留内容
        result = result.replaceAll("<[^>]+>", "");

        // 处理 HTML 实体
        result = result.replaceAll("&nbsp;", " ");
        result = result.replaceAll("&lt;", "<");
        result = result.replaceAll("&gt;", ">");
        result = result.replaceAll("&amp;", "&");
        result = result.replaceAll("&quot;", "\"");
        result = result.replaceAll("&#39;", "'");

        // 清理多余空行
        result = result.replaceAll("\n{3,}", "\n\n");
        result = result.trim();

        return result;
    }

    /**
     * 转换图片标签为 Markdown 格式
     */
    private String convertImgTags(String content, String attachPath) {
        if (content == null) return "";

        Pattern imgPattern = Pattern.compile("<img[^>]+src=\"([^\"]+)\"[^>]*>");
        Matcher matcher = imgPattern.matcher(content);
        StringBuffer sb = new StringBuffer();

        while (matcher.find()) {
            String src = matcher.group(1);
            String fileName = src.substring(src.lastIndexOf('/') + 1);
            // 转换为 Markdown 图片格式
            matcher.appendReplacement(sb, "\n\n![](" + attachPath + "/" + fileName + ")\n\n");
        }
        matcher.appendTail(sb);

        return sb.toString();
    }

    /**
     * 添加附件列表
     * @param md StringBuilder
     * @param attachments 附件列表
     * @param attachPath 附件相对路径 (如 ../attachments/bug/66445)
     */
    private void appendAttachments(StringBuilder md, List<Attachment> attachments, String attachPath) {
        if (attachments == null || attachments.isEmpty()) {
            return;
        }

        md.append("## 附件\n\n");
        for (Attachment att : attachments) {
            if (att.isImage()) {
                md.append("![")
                  .append(att.getFileName())
                  .append("](")
                  .append(attachPath)
                  .append("/")
                  .append(att.getFileName())
                  .append(")\n\n");
            } else {
                md.append("- [")
                  .append(att.getFileName())
                  .append("](")
                  .append(attachPath)
                  .append("/")
                  .append(att.getFileName())
                  .append(")\n");
            }
        }
        md.append("\n");
    }

    private String nullSafe(String value) {
        return value != null ? value : "-";
    }

    /**
     * 清理文件名，移除非法字符
     */
    private String sanitizeFileName(String name) {
        if (name == null) return "unnamed";
        // 移除Windows和Linux不允许的文件名字符
        String sanitized = name.replaceAll("[\\\\/:*?\"<>|]", "_");
        // 限制长度，保留前50个字符
        if (sanitized.length() > 50) {
            sanitized = sanitized.substring(0, 50);
        }
        return sanitized.trim();
    }

    private void writeFile(Path path, String content) throws IOException {
        Files.createDirectories(path.getParent());
        try (Writer writer = new OutputStreamWriter(Files.newOutputStream(path), StandardCharsets.UTF_8)) {
            writer.write(content);
        }
    }
}
