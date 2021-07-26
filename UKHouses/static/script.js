const myDiv = document.getElementById("house")
const myDivError = document.getElementById("house-404")
const myButton = document.getElementById("singleId")

myButton.addEventListener("click", getHouse)
function getHouse() {
  // console.log(myDiv)
  function cleanNode(node) {
    if (!node || !node.firstChild) return
    while (node.firstChild) {
      node.removeChild(node.firstChild)
    }
  }
  cleanNode(myDiv)
  cleanNode(myDivError)

  const API_URL = "http://127.0.0.1:5000/house"

  const ep = document.getElementById("endpoint").value
  endpoint = `${API_URL}/${ep}`

  const responsePromise = fetch(endpoint)
  responsePromise
    .then((data) => data.json())
    // .then((data) => console.log(data))
    .then((house) => showHouse(house))
    // .catch((error) => console.log(error.message))
    .catch((error) => error_404())
}
const error_404 = () => {
  const houseDivError = document.createElement("div-error")
  const housePara = `
  <div>Results:</div>
      <pre>404 Not Found</pre>
      `
  houseDivError.innerHTML = housePara
  myDivError.appendChild(houseDivError)
}

function showHouse(houseObj) {
  const { Id, Code, Price, Date, Postcode, "Property Type": propType, "New built?": newbuilt, "Estate Type": estateType, "House/flat number": number, "Street Address": address, Town, District, County } = houseObj

  const houseDiv = document.createElement("div")
  const housePara = `
  <div>Results:</div>
      <pre>{
            "Id":<span style="color:blue">${Id}</span><br> 
            "Code":<span style="color:green">"${Code}"</span><br> 
            "Price":<span style="color:red">${Price}</span><br> 
            "Date":<span style="color:green">"${Date}"</span><br> 
            "Postcode":<span style="color:green">"${Postcode}"</span><br> 
            "Property Type":<span style="color:green">"${propType}"</span><br> 
            "New built?":<span style="color:green">"${newbuilt}"</span><br> 
            "Estate Type":<span style="color:green">"${estateType}"</span><br> 
            "House/flat number":<span style="color:green">"${number}"</span><br> 
            "Street Address":<span style="color:green">"${address}"</span><br> 
            "Town":<span style="color:green">"${Town}"</span><br> 
            "District":<span style="color:green">"${District}"</span><br> 
            "County":<span style="color:green">"${County}"</span><br>}</pre>
      `
  houseDiv.innerHTML = housePara
  myDiv.appendChild(houseDiv)
  // document.getElementById("endpoint").value = ""
}
