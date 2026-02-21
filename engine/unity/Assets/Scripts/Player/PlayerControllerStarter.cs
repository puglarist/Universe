using UnityEngine;

namespace Universe.Player
{
    [RequireComponent(typeof(CharacterController))]
    public class PlayerControllerStarter : MonoBehaviour
    {
        public float walkSpeed = 4f;
        public float sprintSpeed = 7f;
        public float crouchSpeed = 2f;
        public float jumpForce = 5f;
        public float gravity = -9.81f;

        private CharacterController controller;
        private Vector3 velocity;
        private bool isCrouching;

        private void Awake() => controller = GetComponent<CharacterController>();

        private void Update()
        {
            float h = Input.GetAxis("Horizontal");
            float v = Input.GetAxis("Vertical");
            bool sprint = Input.GetKey(KeyCode.LeftShift);

            if (Input.GetKeyDown(KeyCode.C))
            {
                isCrouching = !isCrouching;
                controller.height = isCrouching ? 1.0f : 2.0f;
            }

            float speed = isCrouching ? crouchSpeed : (sprint ? sprintSpeed : walkSpeed);
            Vector3 move = transform.right * h + transform.forward * v;
            controller.Move(move * speed * Time.deltaTime);

            if (controller.isGrounded && velocity.y < 0)
                velocity.y = -2f;

            if (Input.GetButtonDown("Jump") && controller.isGrounded)
                velocity.y = Mathf.Sqrt(jumpForce * -2f * gravity);

            velocity.y += gravity * Time.deltaTime;
            controller.Move(velocity * Time.deltaTime);
        }
    }
}
