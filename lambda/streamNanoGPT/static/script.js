async function tellStory() {
    const story = document.getElementById("length").value;
  
    if (story.trim().length === 0) {
      return;
    }
  
    const storyOutput = document.getElementById("story-output");
    const percentComplete = document.getElementById("percent-complete");
    const errorOutput = document.getElementById("error-output");
    const rawOutput = document.getElementById("raw-output");
    storyOutput.innerText = "Thinking...";
  
    try {
      // Use Fetch API to send a POST request for response streaming. See https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API 
      const response = await fetch("/api/story", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ "length": story })
      });
  
      storyOutput.innerText = "";
  
      // Response Body is a ReadableStream. See https://developer.mozilla.org/en-US/docs/Web/API/ReadableStream
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      

      // Process the chunks from the stream
      while (true) {
        const { done, value } = await reader.read();
        if (done) {
          break;
        }
        const text = decoder.decode(value);
        //rawOutput.innerText = text;
        multipleOutputs = text.split('}{');
        if (multipleOutputs.length == 1) {
            json = JSON.parse(multipleOutputs[0]); 
            storyOutput.innerText += " " + json.word;
            percentComplete.innerText = json.percentComplete;
        } else {
            json = JSON.parse(multipleOutputs[0] + "}"); 
            storyOutput.innerText += " " + json.word;
            percentComplete.innerText = json.percentComplete;
            for (i = 1; i < multipleOutputs.length - 2; i++) {
                json = JSON.parse("{" + multipleOutputs[i] + "}");
                storyOutput.innerText += " " + json.word;
                percentComplete.innerText = json.percentComplete;
            }
            json = JSON.parse("{" + multipleOutputs[multipleOutputs.length - 1]);
            storyOutput.innerText += " " + json.word;
            percentComplete.innerText = json.percentComplete;
        }
      }
  
    } catch (error) {
      errorOutput.innerText = `Sorry, an error happened. Please try again later. \n\n ${error} \n\n ${error.stack}`;
    }
  
  }
  
  document.getElementById("tell-story").addEventListener("click", tellStory);
  document.getElementById('length').addEventListener('keydown', function (e) {
    if (e.code === 'Enter') {
      tellStory();
    }
  });