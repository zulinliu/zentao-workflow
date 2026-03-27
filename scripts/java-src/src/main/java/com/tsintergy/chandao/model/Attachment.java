package com.tsintergy.chandao.model;

/**
 * 附件实体
 */
public class Attachment {
    private Long id;
    private String title;
    private String pathname;
    private String extension;
    private Long size;
    private String objectType;
    private Long objectId;
    private String addedBy;
    private String addedDate;
    private String downloads;
    
    // 下载后的本地路径
    private String localPath;
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    
    public String getPathname() { return pathname; }
    public void setPathname(String pathname) { this.pathname = pathname; }
    
    public String getExtension() { return extension; }
    public void setExtension(String extension) { this.extension = extension; }
    
    public Long getSize() { return size; }
    public void setSize(Long size) { this.size = size; }
    
    public String getObjectType() { return objectType; }
    public void setObjectType(String objectType) { this.objectType = objectType; }
    
    public Long getObjectId() { return objectId; }
    public void setObjectId(Long objectId) { this.objectId = objectId; }
    
    public String getAddedBy() { return addedBy; }
    public void setAddedBy(String addedBy) { this.addedBy = addedBy; }
    
    public String getAddedDate() { return addedDate; }
    public void setAddedDate(String addedDate) { this.addedDate = addedDate; }
    
    public String getDownloads() { return downloads; }
    public void setDownloads(String downloads) { this.downloads = downloads; }
    
    public String getLocalPath() { return localPath; }
    public void setLocalPath(String localPath) { this.localPath = localPath; }
    
    /**
     * 判断是否为图片
     */
    public boolean isImage() {
        if (extension == null) return false;
        String ext = extension.toLowerCase();
        return ext.equals("jpg") || ext.equals("jpeg") || ext.equals("png") 
            || ext.equals("gif") || ext.equals("bmp") || ext.equals("webp");
    }
    
    /**
     * 获取文件名
     */
    public String getFileName() {
        if (title != null && !title.isEmpty()) {
            return title;
        }
        if (pathname != null && !pathname.isEmpty()) {
            int idx = pathname.lastIndexOf('/');
            if (idx >= 0) {
                return pathname.substring(idx + 1);
            }
            return pathname;
        }
        return "attachment_" + id;
    }
}