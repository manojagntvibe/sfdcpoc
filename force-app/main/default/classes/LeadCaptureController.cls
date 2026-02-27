/**
* @File Name        : LeadCaptureController.cls
* @Description      : Apex controller for Lead Capture LWC; creates Lead and returns score and rating.
* @Author           : Accenture
* @Last Modified By : Accenture
* @Last Modified On : 2025-12-12
* @Modification Log :
**/
public with sharing class LeadCaptureController {

    public class LeadResult {
        @AuraEnabled public Id leadId;
        @AuraEnabled public Decimal leadScore;
        @AuraEnabled public String leadRating;
    }

    /************
    * Name        : createLead
    * Description : Creates a Lead from LWC input, enforces basic validation, and returns score/rating.
    * Parameters  : leadData - Map<String, Object> with lead fields.
    * ReturnType  : LeadResult
    ****************/
    @AuraEnabled
    public static LeadResult createLead(Map<String, Object> leadData) {
        validateAccess();

        Lead newLead = buildLead(leadData);
        insert newLead;

        Lead createdLead = [SELECT Id, Lead_Score__c, Rating FROM Lead WHERE Id = :newLead.Id LIMIT 1];

        LeadResult result = new LeadResult();
        result.leadId = createdLead.Id;
        result.leadScore = createdLead.Lead_Score__c != null ? createdLead.Lead_Score__c : 0;
        result.leadRating = String.isNotBlank(createdLead.Rating) ? createdLead.Rating : 'Cold';
        return result;
    }

    /************
    * Name        : validateAccess
    * Description : Ensures the running user has create permission on Lead.
    * Parameters  : None
    * ReturnType  : void
    ****************/
    private static void validateAccess() {
        if (!Schema.sObjectType.Lead.isCreateable()) {
            throw new AuraHandledException('Insufficient access to create Lead records.');
        }
    }

    /************
    * Name        : buildLead
    * Description : Constructs a Lead from provided map values and sets Channel based on source.
    * Parameters  : leadData - Map<String, Object>
    * ReturnType  : Lead
    ****************/
    private static Lead buildLead(Map<String, Object> leadData) {
        Lead lead = new Lead(); 
        lead.FirstName = (String) leadData.get('FirstName');
        lead.LastName = (String) leadData.get('LastName');
        lead.Email = (String) leadData.get('Email');
        lead.Phone = (String) leadData.get('Phone');
        lead.Company = (String) leadData.get('Company');
        lead.LeadSource = (String) leadData.get('LeadSource');
        lead.Product_Interest__c = (String) leadData.get('ProductInterest');
        lead.Segment__c = (String) leadData.get('Segment');
        lead.Consent__c = (Boolean) leadData.get('Consent');

        if (String.equalsIgnoreCase(lead.LeadSource, 'Website') || String.equalsIgnoreCase(lead.LeadSource, 'Social Media')) {
            lead.Channel__c = 'Digital';
        } else {
            lead.Channel__c = 'Manual';
        }
        return lead;
    }
}