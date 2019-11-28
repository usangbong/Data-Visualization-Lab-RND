using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Valve.VR;
using UnityEngine.SceneManagement;

public class changeScene : MonoBehaviour
{
    public SteamVR_Input_Sources handType;
    public SteamVR_Action_Boolean grabGripAction;
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if(grabGripAction.GetStateDown(handType))
        {
            SceneManager.LoadScene("DirectorScene");
        }
    }
}
