function executeSentence() {
    const sentence = document.getElementById("sentenceInput").value;
    const output = document.getElementById("output");
  
    if (sentence.trim() === "") {
      output.innerText = "Please type something!";
    } else {
      // Open a new Google search tab
      const query = encodeURIComponent(sentence);
      window.open(`https://www.google.com/search?q=${query}`, "_blank");
  
      // Optional: show confirmation in current page
      output.innerText = `Searching for: "${sentence}"`;
    }
  }
  