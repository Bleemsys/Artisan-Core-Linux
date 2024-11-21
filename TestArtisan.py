import subprocess
import unittest
from pathlib import Path

# this script provides an easy access of testing all examples under the .//Test_json// folder. 
# the actual running speed is slower than the execution in the direct command window. 

class TestArtisanMain(unittest.TestCase):
    
    def setUp(self):
        # Define the path using pathlib
        self.test_dir = Path("./Test_json")
        # Directory where the test results are stored
        self.test_results_dir = Path("./Test_results")
        # Counter to track the number of test cases run
        self.run_counter = 0

    def delete_stl_files(self):
        # Find and delete all .stl files in the test_results_dir
        for stl_file in self.test_results_dir.glob("*.stl"):
            try:
                stl_file.unlink()  # Using pathlib's unlink method to delete the file
                print(f"Deleted {stl_file}")
            except Exception as e:
                print(f"Failed to delete {stl_file}: {e}")

    def find_test_files(self):
        # Use pathlib to find all JSON files in the directory and subdirectories
        return list(self.test_dir.rglob("*.json"))
    
    def Predefined_test_files(self):

        testfiles = [
                    '.\\Test_json\\EngineBracket_HS_Infill_Lin_LR.json', 
                    '.\\Test_json\\Basic\\BingDunDun_Infill_LR.json', 
                    '.\\Test_json\\Basic\\Sample_Box.json', 
                    '.\\Test_json\\Basic\\SingleLatticeUnit.json', 
                    '.\\Test_json\\CartesianHexMesh\\GenCartesianHexMesh.json', 
                    '.\\Test_json\\CartesianHexMesh\\GenCartesianHexMesh_vol.json', 
                    # #  '.\\Test_json\\Cases\\FemurCortical\\femur_hex_infill.json', 
                    # #  '.\\Test_json\\Cases\\FemurCortical\\femur_TetConformal_Infill_LR.json', 
                    # #  '.\\Test_json\\Cases\\FluidsDomain\\SphericalFilter_FluidsDomain.json', 
                    # #  '.\\Test_json\\Cases\\FluidsDomain\\SphericalFilter_FluidsDomain_Mesher.json', 
                    # #  '.\\Test_json\\Cases\\SeatSaddle\\SeatSaddle_Hex_Infill.json', 
                    # #  '.\\Test_json\\Cases\\SeatSaddle\\SeatSaddle_Hex_Infill_02.json', 
                    # #  '.\\Test_json\\Cases\\SeatSaddle\\SeatSaddle_Vori_Infill.json', 
                    # #  '.\\Test_json\\Cases\\Shoe\\Shoe_TetConformal_Infill_LR.json', 
                    # #  '.\\Test_json\\Cases\\Shoe_02\\Shoe_GenTetBasicMesh_HexSplit.json', 
                    # '.\\Test_json\\CombinedLattices\\Part02_SingleTPMS.json', 
                    '.\\Test_json\\CombinedLattices\\Parts02_Combined_Infill_LR_conformal.json', 
                    '.\\Test_json\\CombinedLattices\\Parts02_Combined_Infill_LR_conformal_02.json', 
                    '.\\Test_json\\Compression\\EngineBracket_HS_Infill_Lin_LR_Compress.json', 
                    '.\\Test_json\\Compression\\EngineBracket_HS_Infill_Lin_LR_Decompress.json', 
                    '.\\Test_json\\Compression\\Sample_Box.json', 
                    '.\\Test_json\\Compression\\Sample_Box_Decompress.json', 
                    '.\\Test_json\\Compression\\Sample_Box_Infill_Compress.json', 
                    '.\\Test_json\\Compression\\Sample_Box_Infill_Decompress.json', 
                    '.\\Test_json\\ConformalLattice\\Shoe_TetConformal_Infill_LR.json', 
                    '.\\Test_json\\ConformalLattice\\Shoe_TetConformal_Infill_LR_02.json', 
                    '.\\Test_json\\ConformalLattice\\Twisted_Bar_ConformalCustomLattice.json', 
                    '.\\Test_json\\CustomLattice\\BingDunDun_CustomInfill_Geom.json', 
                    '.\\Test_json\\CustomLattice\\BingDunDun_CustomInfill_GeomPlate.json', 
                    '.\\Test_json\\CustomLattice\\BingDunDun_CustomInfill_Strut.json', 
                    '.\\Test_json\\CustomLattice\\BingDunDun_CustomInfill_TPMS.json', 
                    '.\\Test_json\\EngineBracket\\EngineBracket_HS_Infill_Lin_LR.json', 
                    '.\\Test_json\\EngineBracket\\EngineBracket_Strut_Infill_Lin_HR.json', 
                    '.\\Test_json\\EngineBracket\\EngineBracket_Strut_Infill_Lin_LR.json', 
                    '.\\Test_json\\EngineBracket\\EngineBracket_TetConformal_Infill_LR.json', 
                    '.\\Test_json\\FEAMesh\\GenSphericalConformalMesh.json', 
                    '.\\Test_json\\FEAMesh\\Parts02_Export_TPMS_conformal.json', 
                    '.\\Test_json\\FEAMesh\\MeshTrim\\Crankhandle_MeshTrim.json', 
                    '.\\Test_json\\FEAMesh\\MeshTrim_SurfMap\\Crankhandle_MeshTrim_SurfMap.json', 
                    # '.\\Test_json\\FEAMesh\\MeshTrim_SurfMap\\Test.json', 
                    '.\\Test_json\\FEAMesh\\MeshTrim_TPMS\\Crankhandle_MeshTrim_TPMS.json', 
                    '.\\Test_json\\FieldOpt\\Bar_FieldOffset.json', 
                    '.\\Test_json\\FieldOpt\\Box_CornerEnhance.json', 
                    '.\\Test_json\\FieldOpt\\Box_EdgeEnhance.json', 
                    '.\\Test_json\\FieldOpt\\Box_FieldOffsetExpr.json', 
                    '.\\Test_json\\FieldOpt\\Box_FieldOffsetExpr_attractor.json', 
                    '.\\Test_json\\FieldOpt\\Crankhandle_EdgeEnhance.json', 
                    '.\\Test_json\\FieldOpt\\CylinderGradeLattice.json', 
                    '.\\Test_json\\LatticeMerge\\Bar_FieldMerge_Field.json', 
                    '.\\Test_json\\LatticeMerge\\Box_FieldMerge_Annulus.json', 
                    '.\\Test_json\\LatticeMerge\\Box_FieldMerge_Attractor.json', 
                    '.\\Test_json\\LatticeMerge\\Box_FieldMerge_Lin.json', 
                    '.\\Test_json\\LatticeMerge\\Box_FieldMerge_VarSize.json', 
                    '.\\Test_json\\LatticeMerge\\Twisted_Bar_Conformal_MergeLattice.json', 
                    '.\\Test_json\\MeshLattice\\GenCylindricalMesh.json', 
                    '.\\Test_json\\MeshLattice\\GenSphericalMesh.json', 
                    '.\\Test_json\\MeshLattice\\GenTetBasicMesh.json', 
                    '.\\Test_json\\MeshLattice\\GenTetBasicMesh_HexSplit.json', 
                    '.\\Test_json\\MeshLattice\\GenVorMesh.json', 
                    '.\\Test_json\\MeshLattice\\GenVorMesh_crank_handle.json', 
                    '.\\Test_json\\MeshLattice\\GenVorMesh_HexSplit.json', 
                    '.\\Test_json\\MeshLattice\\Parts01_Mesh_Infill_LR.json', 
                    '.\\Test_json\\MeshLattice\\Sample_Box_Mesh.json', 
                    '.\\Test_json\\MeshLattice\\Box_Conformal_MultiSize\\GenCartesianHexMesh_MultiSize.json', 
                    '.\\Test_json\\MeshLattice\\Box_FieldAttractor_MultiSize\\Box_FA_MS.json', 
                    '.\\Test_json\\MeshLattice\\Box_FieldAttractor_MultiSize\\Box_FA_tetmesh_MS.json', 
                    '.\\Test_json\\MeshLattice\\EngineBracket\\EngineBracket_GenTetBasicMesh.json', 
                    '.\\Test_json\\MeshLattice\\EngineBracket\\EngineBracket_GenTetBasicMesh_HexSplit.json', 
                    '.\\Test_json\\MeshLattice\\EngineBracket\\EngineBracket_GenVoriBasicMesh.json', 
                    '.\\Test_json\\MeshLattice\\EngineBracket\\EngineBracket_GenVoriBasicMesh_HexSplit.json',
                     '.\\Test_json\\MeshLattice\\EngineBracket_MultiSize\\EngineBracket_GenTetBasicMesh_HexSplit_MS.json', 
                     '.\\Test_json\\MeshLattice\\ExtMesh\\Mesh_GeomField.json', 
                     '.\\Test_json\\MeshLattice\\ExtractMeshSurf\\ExtractMeshSurf.json', 
                     '.\\Test_json\\MeshLattice\\ExtractMeshSurf\\ExtractMeshSurf_EngineBracket.json', 
                     '.\\Test_json\\MeshLattice\\ExtractMeshSurf\\ExtractSurfMesh_Sphere.json', 
                     '.\\Test_json\\MeshLattice\\FieldDrivenMesh\\FieldDrivenMesh_Attractor.json', 
                     '.\\Test_json\\MeshLattice\\GenSkin\\Crankhandle_MeshTrim_Beam.json', 
                     '.\\Test_json\\MeshLattice\\GenSkin\\Crankhandle_MeshTrim_TPMS.json', 
                     '.\\Test_json\\MeshLattice\\OctTree\\Proc_OctTreeMesh.json', 
                     '.\\Test_json\\MeshLattice\\Remesh\\EngineBracket_Infill_LR.json', 
                     '.\\Test_json\\MeshLattice\\TetwF\\crankhandleTetMesher.json', 
                     '.\\Test_json\\PrimitiveDesign\\GenBox.json', 
                     '.\\Test_json\\PrimitiveDesign\\GenBoxConformalMesh.json', 
                     '.\\Test_json\\PrimitiveDesign\\GenBox_Add.json', 
                     '.\\Test_json\\PrimitiveDesign\\GenBox_Intersection.json', 
                     '.\\Test_json\\PrimitiveDesign\\GenBox_Subtraction.json', 
                     '.\\Test_json\\PrimitiveDesign\\GenCappedConeConformalMesh.json', 
                     '.\\Test_json\\PrimitiveDesign\\GenCylindricalConformalMesh.json', 
                     '.\\Test_json\\PrimitiveDesign\\GenGeom.json', 
                     '.\\Test_json\\PrimitiveDesign\\GenSphericalConformalMesh.json', 
                     '.\\Test_json\\SteeringKnuckle\\SteeringKnuckle_Mesh_Infill_LR.json', 
                     '.\\Test_json\\SurfaceLattice\\BallSurfaceLattice.json', 
                     '.\\Test_json\\SurfaceLattice\\Box_SurfaceLattice.json', 
                     '.\\Test_json\\SurfaceLattice\\Box_SurfaceLattice_02.json', 
                     '.\\Test_json\\SurfaceLattice\\Crankhandle_BasicSurfQuadMesh.json', 
                     '.\\Test_json\\SurfaceLattice\\Crankhandle_SurfaceLattice.json', 
                     '.\\Test_json\\SurfaceLattice\\Gen_BasicSurfQuadMesh.json', 
                     '.\\Test_json\\SurfaceLattice\\GenSimpleQuadMesh.json', 
                     # '.\\Test_json\\Test\\BingDunDun_Infill_LR.json'
                     ]
        
        testfiles_as_paths = [Path(testfile) for testfile in testfiles]

        return testfiles_as_paths

    def test_artisan_main(self):
        # Find all test JSON files
        # test_files = self.find_test_files()
        # only test pre-defined cases
        test_files = self.Predefined_test_files()

        for test_file in test_files:
            # Construct the command to run ArtisanMain.py with each JSON file using pathlib
            # make sure python alias to python3.11
            command = ["python", "ArtisanMain.py", "-f", str(test_file)]
            print("test command: ", command)
            result = subprocess.run(command, capture_output=True, text=True)

            # Assert based on the output or return code
            self.assertEqual(result.returncode, 0, f"Failed for {test_file}")
            print(f"Test {test_file} passed.")

            self.run_counter += 1
            # Every 10 tests, delete the .stl files in ./Test_results/ to save space,
            # you may want to increase the number 10 to some big number for keeping all results.
            if self.run_counter % 10 == 0:
                print("Deleting .stl files after 10 test runs...")
                self.delete_stl_files()
            

if __name__ == '__main__':
    unittest.main()
