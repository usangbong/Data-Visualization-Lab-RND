using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MoveScene : MonoBehaviour
{
   void Update()
    {

        int idx = SceneManager.GetActiveScene().buildIndex;

        if (Input.GetKeyDown(KeyCode.Q))
        {
            //3D
                SceneManager.LoadScene(8);
        }

        else if (Input.GetKeyDown(KeyCode.W))
        {
            //2D
                SceneManager.LoadScene(1);
        }

        else if (Input.GetKeyDown(KeyCode.E))
        {
        //2D
            SceneManager.LoadScene(22);
        }

        else if (Input.GetKeyDown(KeyCode.R))
        {
            //3D
            SceneManager.LoadScene(15);
        }

    }
}
