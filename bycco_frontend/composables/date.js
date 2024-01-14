const date2str = (s) => {
    if (!s) return ""
    // give a localized str version of something that represents a date (not datetime)
    let d = s instanceof Date ? s : new Date(s.substring(0, 10))
    return Intl.DateTimeFormat("en-GB").format(d)
}
const date2iso = (s) => {
    if (!s) return ""
    // give an iSOformat str version of something that represents a date (not datetime)
    let d = s instanceof Date ? s : new Date(s.substring(0, 10))
    return d.toISOString().substring(0, 10)
}
export { date2str, date2iso }









