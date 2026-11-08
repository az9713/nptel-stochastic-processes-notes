window.MathJax = {
  tex: {inlineMath: [['$', '$'], ['\\(', '\\)']], displayMath: [['$$', '$$'], ['\\[', '\\]']],
        processEscapes: true, tags: 'ams'},
  svg: {fontCache: 'local'},
  options: {skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']},
  startup: {pageReady: () => MathJax.startup.defaultPageReady().then(() => {
    document.documentElement.dataset.mathReady = 'true';
  })}
};
