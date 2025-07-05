document.addEventListener("DOMContentLoaded", () => {
  const summarizeBtn = document.getElementById("summarizeBtn");
  const fileInput = document.getElementById("fileInput");
  const summaryBox = document.getElementById("summaryBox");

  summarizeBtn.addEventListener("click", async () => {
    const file = fileInput.files[0];

    if (!file) {
      summaryBox.innerText = "⚠️ Please select a file first.";
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    summaryBox.innerText = "⏳ Summarizing...";

    try {
      const response = await fetch("http://127.0.0.1:8006/summarize", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("❌ Server error");
      }

      const data = await response.text();
      summaryBox.innerText = data;
    } catch (error) {
      summaryBox.innerText = "❌ Failed to summarize. Is the backend running?";
      console.error("Error:", error);
    }
  });
});
