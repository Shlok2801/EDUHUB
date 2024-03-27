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