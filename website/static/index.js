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
    var url = "/enrolled-students?id=" + encodeURIComponent(courseId);       
    window.location.href = url;
}
function unenrollStudent(courseId,userId){           
    fetch('/unenroll-student',{
            method:'POST',
            body: JSON.stringify({courseId: courseId,userId:userId})
    }).then((_res) => {
        var url = "/enrolled-students?id=" + encodeURIComponent(courseId);       
        window.location.href = url;
    });
    
}
function deleteUser(){
    let text = `Do you really want to delete this account ?\n This process is not reversible`;
    if (confirm(text) == true) {            
        fetch('/settings',{
                method:'POST',
        }).then((_res) => {
            window.location.href = '/settings'
        });
    }
}

function downloadAssignment(file){
    console.log("aaaaaaaaaaaaaaaaaa")
    fetch('/download',{
            method:'POST',
            body: JSON.stringify({id: file})
    }).then((_res) => {
        window.location.href = '/assignments-t'
    });
}