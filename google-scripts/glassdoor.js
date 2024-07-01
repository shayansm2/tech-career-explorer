glassdoorSender = '"Glassdoor Jobs"';
var convertglassdoorDataToSheetFormat = getConvertorToSheetFormat("Glassdoor")

function handleGlassdoorEmails() {
  var sheet = SpreadsheetApp.getActive().getSheetByName("Copy of positions")
  var emails = readEmails(glassdoorSender);
  var oldLinks = getPreviousLinks()
  for (var email of emails) {
    var positions = extractGlassdoorData(email);
    positions = positions.filter(element => !oldLinks.includes(element.link))
    for (var row of positions.map(convertglassdoorDataToSheetFormat)) {
      sheet.appendRow(row);
    }
  }
}

function extractGlassdoorData(email) {
  if (email.includes("you have a potential match!")) {
    return extractGlassdoorDetailData(email);
  } else if (email.includes("Your daily job listings for")) {
    return extractGlassdoorListingData(email);
  } else {
    Logger.log("undefined email type: ", email);
  }
}

function extractGlassdoorListingData(email) {
  var result = [];
  var jobs = email.split("[image:");

  const isEasyApplySignature = 'Easy Apply';
  for (var i = 2; i < jobs.length - 1; i++) {
    var job = jobs[i];
    var lines = job.split("\n");

      const linkIndex = lines.findIndex(line => line.includes("<https://www.glassdoor.com/"));

      const data = {
        company: lines[0].split("]")[0],
        position: lines[linkIndex-1],
        link: lines[linkIndex].slice(1, -1),
        location: lines[linkIndex+1],
        easyApply: job.includes(isEasyApplySignature)
      };

      if (job.includes("Staff Software Engineer II - Quality")) {
        console.log(job);
        console.log(job.includes(isEasyApplySignature));
      }

      result.push(data);
  }
  
  return result;
}

function extractGlassdoorDetailData(email) {
  return [];
}