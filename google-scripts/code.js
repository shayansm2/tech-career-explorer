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

function extractLinkedinData(email) {
  const jobs = email.split('---------------------------------------------------------');
  const result = [];

  for (var i = 0; i < jobs.length-1; i ++) {
    var job = jobs[i];    
    if (job.trim() === '') {
      continue;
    }

    const lines = job.split('\n')
                      .map(line => line.trim())
                      .filter(line => line !== '');

    var zeroIndex = 0;
    if (i == 0) {
      zeroIndex = 2;
    }

    const data = {
      position: lines[zeroIndex],
      company: lines[zeroIndex + 1],
      location: lines[zeroIndex + 2],
      link: lines.find(line => line.startsWith('View job:'))
                                    .replace("View job: ", "")
                                    .split("?")[0],
    }

    result.push(data);
  }

  return result;
}

function getMorePositionsUrl(email) {
  const sections = email.split('---------------------------------------------------------');

  var lastSection = sections[sections.length-1];
  var lines = lastSection.split('\n').map(line => line.trim())

  return lines.find(line => line.startsWith('See all jobs on LinkedIn:'))
                                      .replace("See all jobs on LinkedIn: ", "")
                                      .trim();
}

function convertToSheetFormat(data) {
  return [
    "",
    data.location,
    "",
    data.company,
    data.position,
    "todo",
    Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy/MM/dd"),
    "",
    '=HYPERLINK("' + data.link + '", "linkedin")',
  ]
}

function handleLinkedinEmails() {
  var sheet = SpreadsheetApp.getActive().getSheetByName("Copy of positions")
  var linkedinSender = "jobalerts-noreply@linkedin.com";
  var emails = readEmails(linkedinSender)
  for (var email of emails) {
    for (var row of extractLinkedinData(email).map(convertToSheetFormat)) {
      sheet.appendRow(row)
    }
    // console.log("positions are: ", extractLinkedinData(email))
    // console.log("more info is: ", getMorePositionsUrl(email))
  }
}