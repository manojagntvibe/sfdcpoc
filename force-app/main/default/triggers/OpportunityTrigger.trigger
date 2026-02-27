/**
* @File Name        : OpportunityTrigger.trigger
* @Description      : Trigger on Opportunity object. Delegates all logic to OpportunityTriggerHandler
*                     to maintain separation of concerns and single-responsibility principles.
*                     Events handled:
*                       - after insert : Creates a follow-up Task when Type = 'Existing Customer - Replacement'
* @Author           : Accenture
* @Last Modified By : Accenture
* @Last Modified On : 02/26/2026
* @Modification Log :
**/
trigger OpportunityTrigger on Opportunity (after insert) {

    if (Trigger.isAfter && Trigger.isInsert) {
        OpportunityTriggerHandler.handleAfterInsert(Trigger.new);
    }
}
