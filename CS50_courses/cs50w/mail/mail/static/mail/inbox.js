document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');


  // execute send email after compuose form is submitted
  document.querySelector('#compose-form').addEventListener('submit', send_email);

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  display_emails(mailbox);
}

function send_email(event) {
  event.preventDefault();
  
  // Get email data from form inputs
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send email data to server with POST request
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    
    // Load sent mailbox if email was sent successfully
    if (result.message === 'Email sent successfully.') {
      load_mailbox('sent');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

// Get emails from server with GET request
function display_emails(mailbox){
  const emails_view = document.querySelector('#emails-view');
  const email_view = document.querySelector('#email-view');

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);
    // Create email entries and add to email view
    const ul = document.createElement('ul');
    ul.className = 'list-group';
    emails.forEach(email =>{
      const li = document.createElement('li');
      li.className = 'list-group-item list-group-item-action';
      
      // Add CSS class based on whether email has been read or not
      if (email.read) {
        li.classList.add('bg-white');
      } else {
        li.classList.add('bg-light');
      }

      li.innerHTML = `
      <a href='#' class="stretched-link">
      <span class="font-weight-bold">${email.sender}</span>
      ${email.subject}
      <span class="float-right">${email.timestamp}</span>
      </a>
      `;
      li.addEventListener('click', () => view_email(email.id, mailbox));
      ul.appendChild(li);
    });
    emails_view.appendChild(ul);

  })
  .catch(error => {
    console.error('Error:', error);
  });

}


function view_email(email_id, mailbox) {
  // Clear email view
  const email_view = document.querySelector('#email-view');
  email_view.className = 'card';
  email_view.innerHTML = '';
  // Show the email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';


  // get email from using API GET request
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);

    // email header like bootstrap card style
    const div = document.createElement('div');
    div.className = 'card-header';
    div.innerHTML = `
      <h5>${email.subject}</h5>
      <small class="text-muted">From: ${email.sender} | To: ${email.recipients} | ${email.timestamp}</small>
    `;
    email_view.appendChild(div);

    // Using pre for email body, to show same format of body incoming text
    const body = document.createElement('div');
    body.className = 'card-body';
    body.innerHTML = `<pre>${email.body}</pre>`;
    email_view.appendChild(body);

    // Depending on inbox, will be different actions
    const buttons = document.createElement('div');
    buttons.className = 'card-footer';
    if (mailbox === 'inbox') {
      const archive_button = document.createElement('button');
      archive_button.className = 'btn btn-sm btn-outline-primary';
      if (email.archived) {
        archive_button.innerHTML = 'Unarchive';
      } else {
        archive_button.innerHTML = 'Archive';
      }
      archive_button.addEventListener('click', () => toggle_archive_email(email_id, email.archived));
      buttons.appendChild(archive_button);
    } else if (mailbox === 'archive') {
      const unarchive_button = document.createElement('button');
      unarchive_button.className = 'btn btn-sm btn-outline-primary';
      unarchive_button.innerHTML = 'Unarchive';
      unarchive_button.addEventListener('click', () => toggle_archive_email(email_id, true));
      buttons.appendChild(unarchive_button);
    }
    const reply_button = document.createElement('button');
    reply_button.className = 'btn btn-sm btn-outline-primary';
    reply_button.innerHTML = 'Reply';
    reply_button.addEventListener('click', () => reply_email(email));
    buttons.appendChild(reply_button);
    email_view.appendChild(buttons);

    // since clicked on email, mask as read
    mark_email_read(email_id);
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

function mark_email_read(email_id) {
  // cleaning any current view and display the clicked email
  const emails_view = document.querySelector('#emails-view');
  emails_view.innerHTML = '';
  // Make a PUT request to mark email as read
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
  .then(response => {
    console.log(response);
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

function toggle_archive_email(email_id, archived_status) {
  // Put request to change archive status
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !archived_status
    })
  })
  .then(() => {
    load_mailbox('inbox');
  })
  .catch(error => {
    console.error('Error:', error);
  });
  
}

function reply_email(email) {
  // Clear email view
  const emails_view = document.querySelector('#emails-view');
  emails_view.innerHTML = '';


  // checking if the subject starts with Re:
  let subject = email.subject;
  if (!subject.startsWith('Re: ')) {
  subject = `Re: ${subject}`;
  }

  // Pre-fill the replay email fields
  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = `\n \n -------------------------------------------- \n On ${email.timestamp} ${email.sender} wrote:\n${email.body}`;

  // Show composition form and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#compose-form').addEventListener('submit', (event) => {
    event.preventDefault();
    send_email(event.target);
  });
}