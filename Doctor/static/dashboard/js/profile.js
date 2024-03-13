// const fileInput = document.getElementById("upload");
// const imageElement = document.getElementById("image_uploaded");

// function fun5(){
//   document.getElementById("upload").click()
// }

// var update_btn=document.getElementById('update_btn')
// update_btn.addEventListener('click',update_data)


// img_data=document.getElementById('update_update_upload-img').onchange=function(){
//   var f=(this.value);
//   f1 = f.replace(/.*[\/\\]/, '');
//   console.log(f1);
// }




// function update_data(){
//   let img_data=document.getElementById('update_update_upload-img').value.replace(/.*[\/\\]/, '')
//   console.log(img_data);
//   let update_name=document.getElementById('update_name').value;
//   let update_Email=document.getElementById('update_Email').value
//   let update_qualification=document.getElementById('update_qualification').value
//   let update_Speciality=document.getElementById('update_Speciality').value;
//   console.log(update_Speciality);
//   let update_State=document.getElementById('update_State').value;
//   let update_city=document.getElementById('update_city').value;
//   let update_Experience=document.getElementById('update_Experience').value;
//   let update_Mobile=document.getElementById('update_Mobile').value;
//   let update_age=document.getElementById('update_age').value;
//   let update_Fees=document.getElementById('update_Fees').value;
//   let update_gender=document.getElementById('update_gender').value;
//   let update_Language=document.getElementById('update_Language').value;
//   let update_Description=document.getElementById('update_Description').value;

//   // const formData = new FormData();
//   // formData.append('name',update_name)
//   // console.log('----',formData);

//   let xhr = new XMLHttpRequest();

//     console.log(xhr);
//     xhr.onreadystatechange=function(){
//         if (xhr.readyState==4 && xhr.status==200){
//             console.log(xhr);
//         }
//     }
//     xhr.open('POST','/profile/',true)
//     xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  
//     var data='img=' +img_data +"&name="+update_name +"&email="+ update_Email+"&qualification="+update_qualification +"&speciality="+update_Speciality + "&state="+update_State + "&city="+update_city + "&experience=" +update_Experience + "&mobile="+update_Mobile + "&age="+update_age + "&fees=" +update_Fees + "&gender=" +update_gender + "&language="+update_Language +"&description="+update_Description   
//     console.log(data);
    
//     xhr.send(data)

  
  
// }