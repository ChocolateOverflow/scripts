for (var arrScripts = document.getElementsByTagName("script"), i = 0; i < arrScripts.length; i++) {
  if (arrScripts[i].textContent.indexOf("externalId") != -1) {
    const channelId = arrScripts[i].textContent.match(/\"externalId\"\s*\:\s*\"(.*?)\"/,)[1];
    const rss = `https://www.youtube.com/feeds/videos.xml?channel_id=${channelId}`;
    const title = document.getElementById("channel-name").innerText;
    navigator.clipboard.writeText(`${rss} "~${title}"`);
    break;
  }
}
