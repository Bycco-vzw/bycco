const categories = [
  { value: 20, title: "-20", year: 2004 },
  { value: 18, title: "-18", year: 2006 },
  { value: 16, title: "-16", year: 2008 },
  { value: 14, title: "-14", year: 2010 },
  { value: 12, title: "-12", year: 2012 },
  { value: 10, title: "-10", year: 2014 },
  { value: 8, title: "-8", year: 2016 },
]

const languages = ["nl", "fr", "de", "en"]

const yesno = [
  { value: true, text: "Yes" },
  { value: false, text: "No" },
]

const canbechampion = ["Fide Belg.", "No Belg.", "Unknown"]

const trndates = {
  startdate: new Date("2024-04-07"),
  enrollment_start: new Date("2024-01-14 20:00"),
  enrollment_end: new Date("2024-03-31 24:00"),
  lodging_start: new Date("2024-01-04 20:00"),
  // lodging_start: new Date('2024-01-11 20:00'),
}

const roomtypes = []

export { trndates, roomtypes, categories, yesno, canbechampion }
