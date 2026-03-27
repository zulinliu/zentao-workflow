package com.tsintergy.chandao.model;

import java.util.List;

/**
 * 任务实体
 */
public class Task {
    private Long id;
    private String name;
    private String desc;
    private String status;
    private String type;
    private String pri; // 优先级
    private Long project;
    private Long module;
    private Long story;
    private Long storyVersion;
    private Long parent;
    private String openedBy;
    private String openedDate;
    private String assignedTo;
    private String assignedDate;
    private String finishedBy;
    private String finishedDate;
    private String closedBy;
    private String closedDate;
    private String closedReason;
    private Float estimate;
    private Float consumed;
    private Float left;
    private String deadline;
    private String deleted;
    
    // 扩展字段
    private String projectName;
    private String moduleName;
    private String storyTitle;
    private List<Attachment> attachments;
    private List<String> imageUrls;
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public String getDesc() { return desc; }
    public void setDesc(String desc) { this.desc = desc; }
    
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    
    public String getPri() { return pri; }
    public void setPri(String pri) { this.pri = pri; }
    
    public Long getProject() { return project; }
    public void setProject(Long project) { this.project = project; }
    
    public Long getModule() { return module; }
    public void setModule(Long module) { this.module = module; }
    
    public Long getStory() { return story; }
    public void setStory(Long story) { this.story = story; }

    public Long getStoryVersion() { return storyVersion; }
    public void setStoryVersion(Long storyVersion) { this.storyVersion = storyVersion; }

    public Long getParent() { return parent; }
    public void setParent(Long parent) { this.parent = parent; }
    
    public String getOpenedBy() { return openedBy; }
    public void setOpenedBy(String openedBy) { this.openedBy = openedBy; }
    
    public String getOpenedDate() { return openedDate; }
    public void setOpenedDate(String openedDate) { this.openedDate = openedDate; }
    
    public String getAssignedTo() { return assignedTo; }
    public void setAssignedTo(String assignedTo) { this.assignedTo = assignedTo; }
    
    public String getAssignedDate() { return assignedDate; }
    public void setAssignedDate(String assignedDate) { this.assignedDate = assignedDate; }
    
    public String getFinishedBy() { return finishedBy; }
    public void setFinishedBy(String finishedBy) { this.finishedBy = finishedBy; }
    
    public String getFinishedDate() { return finishedDate; }
    public void setFinishedDate(String finishedDate) { this.finishedDate = finishedDate; }
    
    public String getClosedBy() { return closedBy; }
    public void setClosedBy(String closedBy) { this.closedBy = closedBy; }
    
    public String getClosedDate() { return closedDate; }
    public void setClosedDate(String closedDate) { this.closedDate = closedDate; }
    
    public String getClosedReason() { return closedReason; }
    public void setClosedReason(String closedReason) { this.closedReason = closedReason; }
    
    public Float getEstimate() { return estimate; }
    public void setEstimate(Float estimate) { this.estimate = estimate; }
    
    public Float getConsumed() { return consumed; }
    public void setConsumed(Float consumed) { this.consumed = consumed; }
    
    public Float getLeft() { return left; }
    public void setLeft(Float left) { this.left = left; }
    
    public String getDeadline() { return deadline; }
    public void setDeadline(String deadline) { this.deadline = deadline; }
    
    public String getDeleted() { return deleted; }
    public void setDeleted(String deleted) { this.deleted = deleted; }
    
    public String getProjectName() { return projectName; }
    public void setProjectName(String projectName) { this.projectName = projectName; }
    
    public String getModuleName() { return moduleName; }
    public void setModuleName(String moduleName) { this.moduleName = moduleName; }
    
    public String getStoryTitle() { return storyTitle; }
    public void setStoryTitle(String storyTitle) { this.storyTitle = storyTitle; }
    
    public List<Attachment> getAttachments() { return attachments; }
    public void setAttachments(List<Attachment> attachments) { this.attachments = attachments; }
    
    public List<String> getImageUrls() { return imageUrls; }
    public void setImageUrls(List<String> imageUrls) { this.imageUrls = imageUrls; }
}