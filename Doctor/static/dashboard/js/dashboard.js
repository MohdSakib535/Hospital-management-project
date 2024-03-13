function Approved_by_hospital(ele,id){
    var s2=ele.getAttribute('value')
    xhr=new XMLHttpRequest();
    console.log(xhr);
    xhr.onreadystatechange=function(){
        if (xhr.readyState==4 && xhr.status==200){
            var f1=JSON.parse(xhr.responseText)
            console.log(f1);
            if (f1.status==='accept'){
                var d1=ele.parentElement.parentElement
                d1.remove()
            }else{
                console.log('not ');
            }
        }
    }
    xhr.open('POST','/Doctor-data/',true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var data="id="+id + "&value="+s2;
    console.log(data);
    xhr.send(data)
}

function Delete_appointment_data(ele,id){
    var btn_data=ele.getAttribute('value')
    xhr =new XMLHttpRequest();
    xhr.onreadystatechange=function(){
        if(xhr.readyState==4 && xhr.status==200){
            var response_data=JSON.parse(xhr.responseText)
            if(response_data.status==='deleted'){
                var table_row=ele.parentElement.parentElement
                table_row.remove()
            }
        }
    }
   
    xhr.open('POST','/appointment-delete/',true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    var data="id="+id + "&value="+btn_data;
    console.log(data);
    xhr.send(data)
}


function Approved_Appointment_data(ele,appointment_id,patient_id,doctor_id){
    var btn_value=ele.getAttribute('value')
    // console.log(btn_value);
    xhr=new XMLHttpRequest();
    console.log(xhr);
    xhr.onreadystatechange=function(){
        if (xhr.readyState==4 && xhr.status==200){
            var f1=JSON.parse(xhr.responseText)
            // console.log(f1);
            if (f1.status === 'accept'){
                var current_btn=ele.parentElement
                var admitt_btn=ele.parentElement.nextElementSibling
                // console.log(d1);
                // console.log(d7.firstElementChild);
                current_btn.innerHTML=`<input class="btn btn-success delete_btn" id='btn' value='verified'  type='submit'>`
                // console.log(d1);
                admitt_btn.firstElementChild.classList.remove('disabled')

            }else if(f1.status==='reject'){
                var current_btn=ele.parentElement
                var admitt_btn=ele.parentElement.nextElementSibling
                current_btn.innerHTML=`<input class="btn btn-danger delete_btn" id='btn' value='rejected'  type='submit'>`
                admitt_btn.firstElementChild.style.visibility='hidden'
            }
        }
    }
    xhr.open('POST','/doctor-appointment/',true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    var data="appointment_id="+appointment_id +"&patient_id="+ patient_id +"&doctor_id="+doctor_id + "&value="+btn_value 
    // console.log(data);
    xhr.send(data)
}


// function vote_button(ele,id,id2){
//     var app_btn=ele.getAttribute('value')
//     console.log(ele.parentElement);
//     console.log(app_btn);
//     xhr=new XMLHttpRequest();
//     console.log(xhr);
//     xhr.onreadystatechange=function(){
//         if (xhr.readyState==4 && xhr.status==200){
//             var f1=JSON.parse(xhr.responseText)
//             console.log(f1);
//             if (f1.status==='like'){
//                 ele.parentElement.display='none';
//                 ele.parentElement.style.color='green';
//                 var g1=ele.parentElement.parentElement.nextElementSibling.nextElementSibling
//                 // console.log('g1-----',g1);
//                 var g2=g1.querySelector('.like-btn span');
//                 g2.textContent=f1.count
//             }else{
//                 ele.parentElement.style.color='#858796'
//                 var g1=ele.parentElement.parentElement.nextElementSibling.nextElementSibling
//                 // console.log('g1-----',g1);
//                 var g2=g1.querySelector('.like-btn span');
//                 g2.textContent=f1.count
//                 console.log('unlike sata ');
//             }
//         }
//     }
//     xhr.open('POST','/doctor-votes/',true)
//     xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
//     var vote_Data="patient_id="+id +"&doctor_id="+id2+ "&value="+app_btn;
//     console.log(vote_Data);
//     xhr.send(vote_Data)
// }



function vote_button(ele,pid,did){
    var app_btn=ele.getAttribute('value')
    var e1=ele
    var e2=ele.nextElementSibling
    xhr=new XMLHttpRequest();
    console.log(xhr);
    xhr.onreadystatechange=function(){
        if (xhr.readyState==4 && xhr.status==200){
            var l1=JSON.parse(xhr.responseText)
            if (l1.status==='like'){
                // console.log(f1);
                e2.style.color='green'
                e2.style.display='block'
                e1.style.display='none'
                var g1=ele.parentElement.parentElement.nextElementSibling.nextElementSibling
                console.log('g1-----',g1);
                var g2=g1.querySelector('.like-btn span');
                g2.textContent=l1.count
            }
           
        }
    }
    xhr.open('POST','/doctor-votes/',true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var vote_Data="patient_id="+pid +"&doctor_id="+did+ "&value="+app_btn;
    console.log(vote_Data);
    xhr.send(vote_Data)
}



function vote_button2(ele,pid,did){
    var app_btn=ele.getAttribute('value')
    var f1=ele
    var f2=ele.previousElementSibling
    console.log(f1);
    // f1.style.display='none'
    // console.log(f2);
    // f2.style.display='block'
    xhr=new XMLHttpRequest();
    console.log(xhr);
    xhr.onreadystatechange=function(){
        if (xhr.readyState==4 && xhr.status==200){
            var l1=JSON.parse(xhr.responseText)
            if (l1.status==='unlike'){
                f1.style.display='none'
                // console.log(f1);
                f2.style.display='block'
                var g1=ele.parentElement.parentElement.nextElementSibling.nextElementSibling
                console.log('g1-----',g1);
                var g2=g1.querySelector('.like-btn span');
                console.log(g2);
                g2.textContent=l1.count
            }
            
           
        }
    }
    xhr.open('POST','/doctor-votes/',true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var vote_Data="patient_id="+pid +"&doctor_id="+did+ "&value="+app_btn;
    console.log(vote_Data);
    xhr.send(vote_Data)

}



function favourite_doctor_data(element,p1,d1){
    var attr_value=element.getAttribute('value')
    if(attr_value=='bookmark'){
        value_data='bookmark'
        console.log('bookmark');
        xhr=new XMLHttpRequest();
        xhr.onreadystatechange=function(){
            if (xhr.readyState==4 && xhr.status==200){
                var fav_response=JSON.parse(xhr.responseText)
                console.log(fav_response);
                if (fav_response.status=='success'){
                    console.log(element);
                    
                    element.style.color='tomato';
                }else{
                    console.log('unsuccess');
                }  
            }
        }
        

    }else{
        // value_data='already_bookmark'
        value_data=element.getAttribute('fav')
        console.log(value_data);
        
        xhr=new XMLHttpRequest();
        xhr.onreadystatechange=function(){
            if (xhr.readyState==4 && xhr.status==200){
               console.log('already bookmark');   
            //    var g1=element.parentElement.parentElement
            //    console.log(g1);
               var fav_delete_status=JSON.parse(xhr.responseText)
               if(fav_delete_status.status=='delete'){
                element.parentElement.parentElement.remove()
                
               }
            }
        }  
    }
    xhr.open('POST','/my-doctor/',true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var fav_data="patient_id="+p1 +"&doctor_id="+d1+"&value_data="+value_data;
    console.log(fav_data);
    xhr.send(fav_data)
}




function Approved_Appointment(ele,appointment_id,patient_id,doctor_id){
    var app_btn=ele.getAttribute('value')
    var app_btn2=ele.getAttribute('data-Id')
    console.log(app_btn2);
    var text_data=document.getElementById(`floatingTextarea-${app_btn2}`).value
    console.log(text_data);
    xhr=new XMLHttpRequest();
        // console.log(xhr);
        xhr.onreadystatechange=function(){
            if (xhr.readyState==4 && xhr.status==200){
                // console.log(xhr);
                var f1=JSON.parse(xhr.responseText)
                // console.log(f1);
                if(f1.status === 'admit'){
                    var btn_info=ele.parentElement.parentElement.parentElement.parentElement.previousElementSibling
                    btn_info.classList.remove('btn-primary');
                    btn_info.classList.add('btn-success');
                    btn_info.textContent='Admitted'
                    // console.log(btn_info);

                }
            }
        }
        xhr.open('POST','/doctor-appointment/',true)
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        var data="appointment_id="+appointment_id +"&patient_id="+ patient_id +"&doctor_id="+doctor_id + "&value="+app_btn +"&description_data="+text_data;
        console.log(data);
        xhr.send(data)

    const modal = bootstrap.Modal.getInstance(document.querySelector(`#exampleModal-${app_btn2}`));
    // console.log('-----',modal);
    modal.hide();

}


function Discharge_patient(ele,patient_id){
    console.log(ele);
    let xhr = new XMLHttpRequest();
    // console.log(xhr);
    xhr.onreadystatechange=function(){
        if (xhr.readyState==4 && xhr.status==200){
            var discharge_status=JSON.parse(xhr.responseText)
            console.log(discharge_status);
            if (discharge_status.status == 'discharge'){
                let current_ele=ele.parentElement
                console.log(current_ele);
                current_ele.innerHTML=`<button class='btn btn-success' type='submit'>Discharged</button>`
            }else{
                console.log('not discharge');
            }
        }
    }
    xhr.open('POST','/admit-patient/',true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var data='patient_id=' + patient_id 
    xhr.send(data)

}

function Make_charges_data(ele,id,w,u){
    var data_id=ele.getAttribute('data-Id')
    var room_charge=document.getElementById(`room_charges-${data_id}`).value
    var medicine_charges=document.getElementById(`medicine_charges-${data_id}`).value
    var other_charges=document.getElementById(`other_charges-${data_id}`).value
    // console.log(other_charges);
    
    let xhr = new XMLHttpRequest();
    // console.log(xhr);
    xhr.onreadystatechange=function(){
        if (xhr.readyState==4 && xhr.status==200){
            var charges_add=JSON.parse(xhr.responseText)
            console.log(charges_add);
            if (charges_add.status == 'charges_add'){
                let current_ele=ele.parentElement.parentElement.parentElement.parentElement.previousElementSibling
                console.log(current_ele);
                current_ele.parentElement.innerHTML=`<button class='btn btn-success' type='submit'>Added</button>`
                
            }else{
                console.log('not discharge');
            }
        }
    }
    xhr.open('POST','/admit-patient_data/',true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var data='id=' + id + "&room_charge=" +room_charge + "&medicine_charge=" +medicine_charges + "&other_charges=" + other_charges
    // console.log(data);
    xhr.send(data)

    const modal = bootstrap.Modal.getInstance(document.querySelector(`#exampleModal-${data_id}`));
    // console.log('-----',modal);
    modal.hide();


}

function discharge_data_delete(ele,id){
    console.log(ele);
    console.log(id);
    let xhr = new XMLHttpRequest();
    // console.log(xhr);
    xhr.onreadystatechange=function(){
        if (xhr.readyState==4 && xhr.status==200){
            var charges_add=JSON.parse(xhr.responseText)
            // console.log(charges_add);
            if (charges_add.status == 'discharge'){
                let current_ele=ele.parentElement
                console.log(current_ele);
                current_ele.innerHTML=`<button class='btn btn-success' type='submit'>Discharged</button>`
                // current_ele.classList.remove('btn-info');
                // current_ele.classList.add('btn-success');
            }else{
                console.log('not discharge');
            }
        }
    }
    xhr.open('POST','/discharge-patient_dta/',true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var data='id=' + id 
    // console.log(data);
    xhr.send(data)
}



//progress bar admin dashboard

// var t_doctor = document.querySelector('.doctor_count')
// console.log(t_doctor);
// var progress_bar_data=document.getElementById('total_doctor')










