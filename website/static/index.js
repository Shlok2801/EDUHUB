function deleteAssignment(assignmentId,courseId){
    fetch('/delete-assignment',{
            method:'POST',
            body: JSON.stringify({assignmentId: assignmentId})
    }).then((_res) => {
        var url = "/Assignments/" + encodeURIComponent(courseId);       
        window.location.href = url;
    });
}
function deleteSub(submissionId,assignmentId){
    fetch('/delete-sub',{
            method:'POST',
            body: JSON.stringify({submissionId: submissionId})
    }).then((_res) => {
        var url = "/assignments-s/" + encodeURIComponent(assignmentId);       
        window.location.href = url;
    });
}
function deleteMaterial(materialId,courseId){
    fetch('/delete-material',{
            method:'POST',
            body: JSON.stringify({materialId: materialId})
    }).then((_res) => {
        var url = "/Material/" + encodeURIComponent(courseId);       
        window.location.href = url;
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

function unenrollMe(courseId,userId){           
    fetch('/unenroll-me',{
            method:'POST',
            body: JSON.stringify({courseId: courseId,userId:userId})
    }).then((_res) => {       
        window.location.href = "/student-courses"
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