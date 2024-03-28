function deleteAssignment(assignmentId){
    fetch('/delete-assignment',{
            method:'POST',
            body: JSON.stringify({assignmentId: assignmentId})
    }).then((_res) => {
        window.location.href = '/assignments-t'
    });
}
function deleteCourse(courseId){
    let text = `Do you really want to delete this course ${courseId}`;
    if (confirm(text) == true) {       
        fetch('/delete-course',{
                method:'POST',
                body: JSON.stringify({courseId: courseId})
        }).then((_res) => {
            window.location.href = '/manage-t'
        });
    }
}

function enrolledStudents(courseId){      
    fetch('/manage-t',{
            method:'POST',
            body: JSON.stringify({courseId: courseId})
    }).then((response) => {
        if (response.ok) {
          return response.json();
        }})


    // var url = "/enrolled-students?id=" + encodeURIComponent(courseId);       
    // fetch(url)
    // .then(response => {
    //     if (!response.ok) {
    //         throw new Error('Network response was not ok');
    //     }
    //     return response.text();
    // })
    // .then(data => {
    //     // Handle the response data as needed
    //     //window.location.href = "/enrolled-students";
    //     console.log(data);
    // })
    // .catch(error => {
    //     console.error('There was a problem with the fetch operation:', error);
    // });
}