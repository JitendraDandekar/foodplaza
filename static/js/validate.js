function validate(){
	var mobile = document.getElementById("id_contact").value;
	var password = document.getElementById("id_password").value;
	var confirm_password = document.getElementById("id_confirm_password").value;	

	var regex_mobile = /^[7-9]\d{9}$/;
	var regex_password = /^[a-zA-Z0-9!@#$%^&*]{8,}$/;

	if (!regex_mobile.test(mobile)) {
		document.getElementById("id_contact").style.border = "3px solid red";
		return false;
	}
	else if (!regex_password.test(password)){
		document.getElementById("register-error").innerHTML = "<li>Password must be greater than 8 charcaters!</li>"
		return false;
	}
	else if (password !== confirm_password) {
		document.getElementById("register-error").innerHTML = "<li>Password Not Matched!</li>"
		return false;
	}
	else {
		return true;
	}
}