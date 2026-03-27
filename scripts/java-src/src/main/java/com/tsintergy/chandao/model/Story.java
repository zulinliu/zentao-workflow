package com.tsintergy.chandao.model;

import java.util.List;

/**
 * 需求实体
 */
public class Story {
    private Long id;
    private String title;
    private String spec;
    private String verify;
    private String status;
    private String stage;
    private String pri; // 优先级
    private String source;
    private String category;
    private Long product;
    private Long module;
    private Long plan;
    private Long project;
    private String openedBy;
    private String openedDate;
    private String assignedTo;
    private String assignedDate;
    private String closedBy;
    private String closedDate;
    private String closedReason;
    private Long parent;
    private Long parentVersion;
    private String version;
    private String deleted;
    
    // 扩展字段
    private String productName;
    private String moduleName;
    private String projectName;
    private List<Attachment> attachments;
    private List<String> imageUrls;
    
    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    
    public String getSpec() { return spec; }
    public void setSpec(String spec) { this.spec = spec; }
    
    public String getVerify() { return verify; }
    public void setVerify(String verify) { this.verify = verify; }
    
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    
    public String getStage() { return stage; }
    public void setStage(String stage) { this.stage = stage; }
    
    public String getPri() { return pri; }
    public void setPri(String pri) { this.pri = pri; }
    
    public String getSource() { return source; }
    public void setSource(String source) { this.source = source; }
    
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    
    public Long getProduct() { return product; }
    public void setProduct(Long product) { this.product = product; }
    
    public Long getModule() { return module; }
    public void setModule(Long module) { this.module = module; }
    
    public Long getPlan() { return plan; }
    public void setPlan(Long plan) { this.plan = plan; }
    
    public Long getProject() { return project; }
    public void setProject(Long project) { this.project = project; }
    
    public String getOpenedBy() { return openedBy; }
    public void setOpenedBy(String openedBy) { this.openedBy = openedBy; }
    
    public String getOpenedDate() { return openedDate; }
    public void setOpenedDate(String openedDate) { this.openedDate = openedDate; }
    
    public String getAssignedTo() { return assignedTo; }
    public void setAssignedTo(String assignedTo) { this.assignedTo = assignedTo; }
    
    public String getAssignedDate() { return assignedDate; }
    public void setAssignedDate(String assignedDate) { this.assignedDate = assignedDate; }
    
    public String getClosedBy() { return closedBy; }
    public void setClosedBy(String closedBy) { this.closedBy = closedBy; }
    
    public String getClosedDate() { return closedDate; }
    public void setClosedDate(String closedDate) { this.closedDate = closedDate; }
    
    public String getClosedReason() { return closedReason; }
    public void setClosedReason(String closedReason) { this.closedReason = closedReason; }
    
    public Long getParent() { return parent; }
    public void setParent(Long parent) { this.parent = parent; }
    
    public Long getParentVersion() { return parentVersion; }
    public void setParentVersion(Long parentVersion) { this.parentVersion = parentVersion; }
    
    public String getVersion() { return version; }
    public void setVersion(String version) { this.version = version; }
    
    public String getDeleted() { return deleted; }
    public void setDeleted(String deleted) { this.deleted = deleted; }
    
    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }
    
    public String getModuleName() { return moduleName; }
    public void setModuleName(String moduleName) { this.moduleName = moduleName; }
    
    public String getProjectName() { return projectName; }
    public void setProjectName(String projectName) { this.projectName = projectName; }
    
    public List<Attachment> getAttachments() { return attachments; }
    public void setAttachments(List<Attachment> attachments) { this.attachments = attachments; }
    
    public List<String> getImageUrls() { return imageUrls; }
    public void setImageUrls(List<String> imageUrls) { this.imageUrls = imageUrls; }
}