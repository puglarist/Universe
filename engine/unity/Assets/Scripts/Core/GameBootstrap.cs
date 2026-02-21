using UnityEngine;

namespace Universe.Core
{
    public class GameBootstrap : MonoBehaviour
    {
        [SerializeField] private string worldSceneName = "Origin Map";

        private void Start()
        {
            Debug.Log($"Universe bootstrap loaded. Active world: {worldSceneName}");
            Physics.gravity = new Vector3(0, -9.81f, 0);
        }
    }
}
