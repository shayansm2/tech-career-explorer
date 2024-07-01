const linkedinSender = "jobalerts-noreply@linkedin.com";
const divider = "---------------------------------------------------------";
var convertLinkedinDataToSheetFormat = getConvertorToSheetFormat("Linkedin")

function handleLinkedinEmails() {
  var sheet = SpreadsheetApp.getActive().getSheetByName("Copy of positions")
  var emails = readEmails(linkedinSender);
  var oldLinks = getPreviousLinks()
  for (var email of emails) {
    var positions = extractLinkedinData(email);
    positions = positions.filter(element => !oldLinks.includes(element.link))
    for (var row of positions.map(convertLinkedinDataToSheetFormat)) {
      sheet.appendRow(row);
    }
    // console.log(positions);
    // break;
    // console.log("more info is: ", getMorePositionsUrl(email))
  }
}

function extractLinkedinData(email) {
  const jobs = email.split(divider);
  var result = [];

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

    // Logger.log(lines);

    const jolUrlSignature = 'View job: ';
    const isEasyApplySignature = 'Apply with resume & profile';
    const data = {
      position: lines[zeroIndex],
      company: lines[zeroIndex + 1],
      location: lines[zeroIndex + 2],
      link: lines.find(line => line.startsWith(jolUrlSignature))
                                    .replace(jolUrlSignature, "")
                                    .split("?")[0],
      easyApply: lines.includes(isEasyApplySignature),
    }

    result.push(data);
  }

  return result;
}

function getMorePositionsUrl(email) {
  const sections = email.split(divider);

  var lastSection = sections[sections.length-1];
  var lines = lastSection.split('\n').map(line => line.trim())

  const moreUrlSignature = 'See all jobs on LinkedIn: ';
  return lines.find(line => line.startsWith(moreUrlSignature))
                                      .replace(moreUrlSignature, "")
                                      .trim();
}