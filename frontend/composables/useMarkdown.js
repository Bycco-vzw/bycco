import showdown from 'showdown'
import fm from 'front-matter'
const mdConverter = new showdown.Converter({ metadata: true })

export const useMarkdown = (content) => {
  let html
  try {
    html = mdConverter.makeHtml(content)
  }
  catch (error) {
    console.error("cannot convert markdown", error)
  }
  const metadata = fm(content).attributes
  console.log('html', html)
  return {
    html,
    metadata,
  }
}


