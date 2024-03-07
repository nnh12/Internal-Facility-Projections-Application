function getFormId(key, field_name) {
    return "#" + key + "_" + field_name
}


class ProjectionFormData {
    constructor(projection, comments, accountParentLevelE, account, activity, program, location) {
        this.projection = projection;
        this.comments = comments;
        this.accountParentLevelE = accountParentLevelE;
        this.account = account;
        this.activity = activity;
        this.program = program;
        this.location = location;
    }
}

function commaFormat(value){
    return value.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
}

function createProjectionFormObjects(forms) {
    var objs = [];
    for (let i = 0; i < forms.length; i++) {
        var form = forms[i];
        var key = $(form).attr("data-key");

        let projection = convertCurrencyToInt($(getFormId(key, "projection")).val());
        let comments = $(getFormId(key, "comments")).val();
        let accountParentLevelE = $(getFormId(key, "accountParentLevelE")).val();
        let account =  $(getFormId(key, "account")).val();
        let program =  null;
        let location =  null;
        let activity =  null;
        if ($(getFormId(key, "program")).length  !== 0){
            program = $(getFormId(key, "program")).text().trim();
        }

        if ($(getFormId(key, "location")).length !== 0){
            location = $(getFormId(key, "location")).text().trim();
        }

        if ($(getFormId(key, "activity")).length !== 0){
            activity = $(getFormId(key, "activity")).text().trim();
        }

        objs[i] = JSON.stringify(new ProjectionFormData(projection, comments, accountParentLevelE, account, activity, program, location));

    }
    return objs;
}

function submitForm(forms, url, csrf_token) {
    //Submits the specified form via AJAX

    //Takes the key which is the prefix for all form field ids

    $.ajax({
        type: "POST",
        url: url,
        data: {
            //Uses prefix + IDs to get the entered value for each form field to submit.
            //Django will receive a post request with these in the request.POST method.
            'forms[]': forms,
            csrfmiddlewaretoken: csrf_token,
            dataType: "json",

        },
        success: function (data) {
            //Received a status 200 - SUCCESS (uses a JSONResponse from Django)
            console.log("success");
        },

        failure: function () {
            //Received a status 400 - FAIL (uses a JSONResponse from Django)
            console.log("failed to post...");
        }
    });
}

function disableSubmitButton() {
    $("#submitButton").prop("disabled", true);
}

function allRequiredInputsAreFilled() {
    var inputs = $('input');
    for (let i = 0; i < inputs.length; i++) {
        var currentInput = $(inputs[i]);
        if (currentInput.prop("required") && !currentInput.val()) {
            return false;
        }
    }
    return true;
}

function determineSubmitButtonDisabledState() {
    enableSubmitButton();
    if (!allRequiredInputsAreFilled()) {
        disableSubmitButton();
    }
}
/**
 * Takes string as input and will covert it to a float value
 * @param text
 * @returns {number}
 */
function convertCurrencyToInt(text) {
    var result = 0;
    if (typeof text === 'number'){
        return int(text);
    }
    if(text) {
        //Negative values are represented using '(val)' format. Positive values do not have the brackets
        if (text.includes("(") || text.includes(")")) {
            result = -1 * parseInt(text.replaceAll('(', '').replaceAll(')', '').replaceAll(',', ''));
        } else {
            result = parseInt(text.replaceAll(',', ''));
        }
    }

    if (isNaN(result)){
        return 0;
    }
    return result;
}
 /**
 * Updates the net budget field for each projection form row
 */
function updateNetBudget(){
    var forms = $('.projectionForm');

    for (let i = 0; i < forms.length; i++) {
        var key = $(forms[i]).attr("data-key");
        updateNetBudgetFieldWithKey(key);
    }

}
/**
 * Given a provided key (stored in the data-key attr of the form) to identify the attribute, update it's netBudget field
 * @param key
 */
function updateNetBudgetFieldWithKey(key) {
    let netBudgetField = $(getFormId(key, "netBudget"));
    let budgetAmount = $(getFormId(key, "budgetAmount"));
    let projection = $(getFormId(key, "projection"));

    var budgetValue = convertCurrencyToInt(budgetAmount.text());
    var projectionValue = convertCurrencyToInt(projection.val());

    //Update the net budget field
    var updatedValue = budgetValue - projectionValue;
    netBudgetField.val(updatedValue);
    formatCurrencyField(projection, 'black', 'red');
    formatCurrencyField(netBudgetField, 'black', 'red');

}

/**
 * Color formats a field depending on whether it is positive or negative in value
 * @param field
 * @param successColor
 * @param failColor
 */
function formatCurrencyField(field, successColor, failColor) {
    var valueRaw = convertCurrencyToInt(field.val());
    var currentValue = commaFormat(parseFloat(valueRaw).toFixed(0));
    if (convertCurrencyToInt(field.val()) < 0) {

        field.css('color', failColor);

        if (currentValue.indexOf("(") === -1){
            //Omits the '-' sign in the value
            $(field).val("(" + currentValue.slice(1) + ")");
        }

    } else {
        field.css('color', successColor);
        $(field).val(currentValue);
    }

}

function formatCurrencyFieldText(text) {
    var valueRaw = convertCurrencyToInt(text);
    var currentValue = commaFormat(parseFloat(valueRaw).toFixed(0));
    var result = "";
    if (convertCurrencyToInt(text) < 0) {

        if (currentValue.indexOf("(") === -1){
            //Omits the '-' sign in the value
            result = "(" + currentValue.slice(1) + ")";
        }

    } else {
        result = currentValue;
    }

    return result;

}



