import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'page-privacy',
  standalone: true,
  imports: [CommonModule],
  template: `
    
    <!-- Page header -->
    <div class="page-header d-print-none">
      <div class="container-xl">
        <div class="row g-2 align-items-center">
          <div class="col">
            <h2 class="page-title">
              Privacy & Cookie Policy
            </h2>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Page content -->
    <div class="page-body">
      <div class="container-xl">
        <div class="row justify-content-center">
          <div class="col-lg-10 col-xl-9">
            <div class="card card-lg">
              <div class="card-body markdown">
                
                <p>Effective date: June 24, 2023</p>

                <h1>Introduction</h1>
                <p>
                  Thank you for visiting Lifetracker. We are committed to protecting your privacy and safeguarding your personal information. This Privacy and Cookie Policy explains how we collect, use, and disclose the personal information you provide when registering on our website.
                </p>

                <h1>Personal Information Collection</h1>
                <p>During the registration process, we collect the following personal information from you:</p>
                  <ul>
                    <li>Name</li>
                    <li>Email address</li>
                    <li>Password</li>
                  </ul>

                <h1>Purpose of Collection</h1>
                <p>We collect your personal information for the following purposes:</p>
                  <ul>
                    <li>To create and maintain your user account</li>
                    <li>To communicate with you regarding updates, notifications, and information related to our services</li>
                  </ul>
                
                <h1>Consent</h1>
                <p>By registering on our website and providing us with your personal information, you consent to the collection, use, and disclosure of that information as described in this Privacy and Cookie Policy.</p>

                <h1>Use and Disclosure</h1>
                <p>We use the collected personal information solely for the purposes stated above. We do not disclose your personal information to third parties without your explicit consent, except as required by law.</p>

                <h1>Security</h1>
                <p>
                  We take reasonable precautions and implement appropriate security measures to protect your personal information from unauthorized access, disclosure, or alteration. However, please note that no data transmission over the internet can be guaranteed as completely secure.
                </p>

                <h1>Cookies</h1>
                <p>
                  Our website uses cookies to enhance your browsing experience. Cookies are small text files stored on your device when you visit our website. We use cookies to analyze website traffic, personalize content, and improve our services. By using our website, you consent to the use of cookies in accordance with this Privacy and Cookie Policy. You have control over what cookies websites place on your computer through your browser settings.
                </p>

                <h1>Third-Party Services</h1>
                <p>
                  We may use third-party services, such as analytics or advertising platforms, that may collect and process your personal information. These third parties have their own privacy policies, and we encourage you to review them. We are not responsible for the privacy practices or content of these third-party services.
                </p>

                <h1>Access and Correction</h1>
                <p>
                  You have the right to access and correct your personal information stored on our website. You can update your account details by logging into your user account or contact us directly to request changes.
                </p>

                <h1>Retention</h1>
                <p>
                  We retain your personal information for as long as necessary to fulfill the purposes outlined in this Privacy and Cookie Policy, unless a longer retention period is required or permitted by law.
                </p>

                <h1>Compliance with Laws</h1>
                <p>
                  We comply with applicable Canadian privacy laws, including the Personal Information Protection and Electronic Documents Act (PIPEDA) and provincial privacy legislation. You have certain rights under these laws, such as the right to access your personal information and request its correction or deletion.
                </p>

                <h1>Changes to the Policy</h1>
                <p>
                  We reserve the right to modify or update this Privacy and Cookie Policy at any time. Any changes will be effective upon posting the revised policy on our website. We recommend reviewing this policy periodically to stay informed of our privacy practices.
                </p>

                <h1>Contact Information</h1>
                <p>
                  If you have any questions, concerns, or requests regarding this Privacy and Cookie Policy, please contact us at <a href="mailto:jason@thevriends.com">jason@thevriends.com</a>.
                </p>                   

              </div>
            </div>
          </div>
        </div>
      </div>
  `,
  styles: [
  ]
})
export class PrivacyComponent {

}
