using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using Valve.VR;

public class ChangeDot : MonoBehaviour
{
    public SteamVR_Input_Sources handType;
    public SteamVR_Action_Boolean grabgripAction;
    public SteamVR_Action_Boolean grabPinchAction;

    MoveObject moveObject = GameObject.Find("GameObject").GetComponent<MoveObject>();

    void Update()
    {
        if (grabgripAction.GetStateDown(handType))
        {
            SceneManager.LoadScene("Director Dot Scene");
        }

        if(grabPinchAction.GetStateDown(handType))
        {
            moveObject.isMove = true;
        }
    }
}
