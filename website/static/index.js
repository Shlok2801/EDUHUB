function deleteAssignment(assignmentId){
    fetch('/delete-assignment',{
            method:'POST',
            body: JSON.stringify({assignmentId: assignmentId})
    }).then((_res) => {
        window.location.href = '/assignments-t'
    });
}