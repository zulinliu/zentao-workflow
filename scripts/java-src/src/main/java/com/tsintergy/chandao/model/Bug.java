package com.tsintergy.chandao.model;

import java.util.List;

/**
 * Bug实体
 */
public class Bug {
    private Long id;
    private String title;
    private String steps;
    private String status;
    private String confirmed;
    private String pri; // 优先级
    private String severity;
    private String type;
    private Long product;
    private Long module;
    private Long project;
    private Long story;
    private Long task;
    private String openedBy;
    private String openedDate;
    private String assignedTo;
    private String assignedDate;
    private String resolvedBy;
    private String resolvedDate;
    private String resolution;
    private String closedBy;
    private String closedDate;
    private Long duplicateBug;
    private String deadline;
    private String deleted;
    
    // 扩展字段
    private String productName;
    private String moduleName;
    private String projectName;
    private String storyTitle;
    private List<Attachment> attachments;
    private List<String> imageUrls;
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    
    public String getSteps() { return steps; }
    public void setSteps(String steps) { this.steps = steps; }
    
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    
    public String getConfirmed() { return confirmed; }
    public void setConfirmed(String confirmed) { this.confirmed = confirmed; }
    
    public String getPri() { return pri; }
    public void setPri(String pri) { this.pri = pri; }
    
    public String getSeverity() { return severity; }
    public void setSeverity(String severity) { this.severity = severity; }
    
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    
    public Long getProduct() { return product; }
    public void setProduct(Long product) { this.product = product; }
    
    public Long getModule() { return module; }
    public void setModule(Long module) { this.module = module; }
    
    public Long getProject() { return project; }
    public void setProject(Long project) { this.project = project; }
    
    public Long getStory() { return story; }
    public void setStory(Long story) { this.story = story; }
    
    public Long getTask() { return task; }
    public void setTask(Long task) { this.task = task; }
    
    public String getOpenedBy() { return openedBy; }
    public void setOpenedBy(String openedBy) { this.openedBy = openedBy; }
    
    public String getOpenedDate() { return openedDate; }
    public void setOpenedDate(String openedDate) { this.openedDate = openedDate; }
    
    public String getAssignedTo() { return assignedTo; }
    public void setAssignedTo(String assignedTo) { this.assignedTo = assignedTo; }
    
    public String getAssignedDate() { return assignedDate; }
    public void setAssignedDate(String assignedDate) { this.assignedDate = assignedDate; }
    
    public String getResolvedBy() { return resolvedBy; }
    public void setResolvedBy(String resolvedBy) { this.resolvedBy = resolvedBy; }
    
    public String getResolvedDate() { return resolvedDate; }
    public void setResolvedDate(String resolvedDate) { this.resolvedDate = resolvedDate; }
    
    public String getResolution() { return resolution; }
    public void setResolution(String resolution) { this.resolution = resolution; }
    
    public String getClosedBy() { return closedBy; }
    public void setClosedBy(String closedBy) { this.closedBy = closedBy; }
    
    public String getClosedDate() { return closedDate; }
    public void setClosedDate(String closedDate) { this.closedDate = closedDate; }
    
    public Long getDuplicateBug() { return duplicateBug; }
    public void setDuplicateBug(Long duplicateBug) { this.duplicateBug = duplicateBug; }
    
    public String getDeadline() { return deadline; }
    public void setDeadline(String deadline) { this.deadline = deadline; }
    
    public String getDeleted() { return deleted; }
    public void setDeleted(String deleted) { this.deleted = deleted; }
    
    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }
    
    public String getModuleName() { return moduleName; }
    public void setModuleName(String moduleName) { this.moduleName = moduleName; }
    
    public String getProjectName() { return projectName; }
    public void setProjectName(String projectName) { this.projectName = projectName; }
    
    public String getStoryTitle() { return storyTitle; }
    public void setStoryTitle(String storyTitle) { this.storyTitle = storyTitle; }
    
    public List<Attachment> getAttachments() { return attachments; }
    public void setAttachments(List<Attachment> attachments) { this.attachments = attachments; }
    
    public List<String> getImageUrls() { return imageUrls; }
    public void setImageUrls(List<String> imageUrls) { this.imageUrls = imageUrls; }
}