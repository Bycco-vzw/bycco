import showdown from 'showdown'
import fm from 'front-matter'
const mdConverter = new showdown.Converter({ metadata: true })

export const useMarkdown = (content) => {
  const html = mdConverter.makeHtml(content)
  const metadata = fm(content).attributes
  return {
    html,
    metadata,
  }
}


