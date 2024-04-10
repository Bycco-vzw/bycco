const l = window.location
console.log('checking hostname', l.hostname)
if (l.hostname == "bycco.be") {
  console.log('redirecting')
  location.replace(`${l.protocol}//www.bycco.be${l.pathname}${l.search}`)
}