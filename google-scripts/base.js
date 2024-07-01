function readEmails(sender, daysToRead = 1) {
    var now = new Date();
    var lastNDays = new Date(now.getTime() - (daysToRead * 24 * 60 * 60 * 1000));
  
      var inbox = GmailApp.search(
        'from:' + sender + 
        ' after:' + Utilities.formatDate(lastNDays, Session.getScriptTimeZone(), "yyyy/MM/dd")
      );
  
    var result = [];
    for (var i = 0; i < inbox.length; i++) {
      var messages = inbox[i].getMessages();
      for (var j = 0; j < messages.length; j++) {
        var message = messages[j];
        result.push(message.getPlainBody())
      }
    }
    return result
  }
  
  function getPreviousLinks() {
    var sheet = SpreadsheetApp.getActive().getSheetByName("Copy of positions")
    var range = sheet.getRange("I:I");
    var values = range.getRichTextValues();
  
    var result = [];
    for (var i = 0; i < values.length; i++) {
      var link = values[i][0].getLinkUrl();
      if (link != null) {
        result.push(link);
      }
    }
  
    return result;
  }
  
  function getConvertorToSheetFormat(source) {
    return function(data) {
      let linkTitle = source;
      if (data.easyApply) {
        linkTitle = source + " easy apply";
      }
  
      return [
        "",
        data.location,
        "",
        data.company,
        data.position,
        "todo",
        Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy/MM/dd"),
        "",
        '=HYPERLINK("' + data.link + '", "' + linkTitle + '")',
      ]
    }
  }